#!/usr/bin/env python3
"""
Detailed Professional Report Generator
- Executive summary
- Detailed tables
- Statistical analysis
- Trend analysis with tables
- Recommendations with tables
"""
import pandas as pd
import numpy as np
import json
import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from scipy import stats

class DetailedReportGenerator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.numeric_cols = []
        self.categorical_cols = []
        self.datetime_cols = []
        
    def load_data(self):
        """Load and analyze data"""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            else:
                self.df = pd.read_excel(self.filepath)
            
            # Categorize columns
            for col in self.df.columns:
                try:
                    pd.to_numeric(self.df[col], errors='raise')
                    self.numeric_cols.append(col)
                except:
                    if self.df[col].nunique() < 50:
                        self.categorical_cols.append(col)
            
            return True
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return False
    
    def generate_pdf(self, output_filename):
        """Generate detailed professional PDF"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(script_dir, '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        output_path = os.path.join(reports_dir, output_filename)
        
        # Use landscape for more table space
        doc = SimpleDocTemplate(output_path, pagesize=landscape(letter),
                               topMargin=0.5*inch, bottomMargin=0.5*inch,
                               leftMargin=0.5*inch, rightMargin=0.5*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        # COVER PAGE
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph("📊 DETAILED ANALYTICS REPORT", title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              styles['Normal']))
        story.append(Paragraph(f"Dataset: {os.path.basename(self.filepath)}", styles['Normal']))
        story.append(PageBreak())
        
        # EXECUTIVE SUMMARY
        story.append(Paragraph("📋 EXECUTIVE SUMMARY", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        summary_data = [
            ['Metric', 'Value', 'Details'],
            ['Total Records', f"{len(self.df):,}", f"Complete dataset with {len(self.df):,} data points"],
            ['Total Variables', str(len(self.df.columns)), f"{len(self.numeric_cols)} numeric, {len(self.categorical_cols)} categorical"],
            ['Numeric Columns', str(len(self.numeric_cols)), ', '.join(self.numeric_cols[:5]) + ('...' if len(self.numeric_cols) > 5 else '')],
            ['Categorical Columns', str(len(self.categorical_cols)), ', '.join(self.categorical_cols[:5]) + ('...' if len(self.categorical_cols) > 5 else '')],
            ['Data Completeness', f"{(1 - self.df.isnull().sum().sum()/(len(self.df)*len(self.df.columns)))*100:.1f}%", 
             f"{self.df.isnull().sum().sum():,} missing values out of {len(self.df)*len(self.df.columns):,} total"],
            ['Date Range', self._get_date_range(), 'Based on datetime columns if available']
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch, 5*inch])
        summary_table.setStyle(self._get_header_table_style())
        story.append(summary_table)
        story.append(PageBreak())
        
        # DETAILED COLUMN ANALYSIS
        story.append(Paragraph("📊 DETAILED COLUMN ANALYSIS", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        col_data = [['Column Name', 'Data Type', 'Unique Values', 'Missing', 'Min', 'Max', 'Mean', 'Std Dev']]
        
        for col in self.df.columns[:30]:  # Limit to 30 columns
            row = [col]
            
            # Data type
            if col in self.numeric_cols:
                row.append('Numeric')
            elif col in self.categorical_cols:
                row.append('Categorical')
            else:
                row.append('Text')
            
            # Unique values
            row.append(str(self.df[col].nunique()))
            
            # Missing
            missing_pct = (self.df[col].isna().sum() / len(self.df)) * 100
            row.append(f"{missing_pct:.1f}%")
            
            # Stats for numeric
            if col in self.numeric_cols:
                row.append(f"{self.df[col].min():.2f}")
                row.append(f"{self.df[col].max():.2f}")
                row.append(f"{self.df[col].mean():.2f}")
                row.append(f"{self.df[col].std():.2f}")
            else:
                row.extend(['N/A', 'N/A', 'N/A', 'N/A'])
            
            col_data.append(row)
        
        col_table = Table(col_data, colWidths=[1.5*inch, 1*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        col_table.setStyle(self._get_header_table_style())
        story.append(col_table)
        story.append(PageBreak())
        
        # STATISTICAL SUMMARY
        if self.numeric_cols:
            story.append(Paragraph("📈 STATISTICAL SUMMARY", heading_style))
            story.append(Spacer(1, 0.1*inch))
            
            stat_data = [['Metric'] + self.numeric_cols[:6]]  # Top 6 numeric columns
            
            metrics = ['Count', '25th Percentile', 'Median (50th)', '75th Percentile', 'Mean', 'Std Deviation', 'Variance', 'Skewness', 'Kurtosis']
            
            for metric in metrics:
                row = [metric]
                for col in self.numeric_cols[:6]:
                    if metric == 'Count':
                        row.append(f"{self.df[col].count():,}")
                    elif metric == '25th Percentile':
                        row.append(f"{self.df[col].quantile(0.25):.2f}")
                    elif metric == 'Median (50th)':
                        row.append(f"{self.df[col].median():.2f}")
                    elif metric == '75th Percentile':
                        row.append(f"{self.df[col].quantile(0.75):.2f}")
                    elif metric == 'Mean':
                        row.append(f"{self.df[col].mean():.2f}")
                    elif metric == 'Std Deviation':
                        row.append(f"{self.df[col].std():.2f}")
                    elif metric == 'Variance':
                        row.append(f"{self.df[col].var():.2f}")
                    elif metric == 'Skewness':
                        row.append(f"{self.df[col].skew():.2f}")
                    elif metric == 'Kurtosis':
                        row.append(f"{self.df[col].kurtosis():.2f}")
                stat_data.append(row)
            
            stat_table = Table(stat_data)
            stat_table.setStyle(self._get_header_table_style())
            story.append(stat_table)
            story.append(PageBreak())
        
        # CATEGORICAL ANALYSIS
        if self.categorical_cols:
            story.append(Paragraph("📊 CATEGORICAL DISTRIBUTION ANALYSIS", heading_style))
            story.append(Spacer(1, 0.1*inch))
            
            for cat_col in self.categorical_cols[:3]:
                story.append(Paragraph(f"<b>{cat_col}</b>", styles['Heading3']))
                
                value_counts = self.df[cat_col].value_counts().head(15)
                total = len(self.df)
                
                cat_data = [['Category', 'Count', 'Percentage', 'Cumulative %']]
                cumulative = 0
                
                for idx, (cat, count) in enumerate(value_counts.items()):
                    pct = (count / total) * 100
                    cumulative += pct
                    cat_data.append([
                        str(cat)[:30],
                        f"{count:,}",
                        f"{pct:.1f}%",
                        f"{cumulative:.1f}%"
                    ])
                
                cat_table = Table(cat_data, colWidths=[3*inch, 1.5*inch, 1.5*inch, 1.5*inch])
                cat_table.setStyle(self._get_striped_table_style())
                story.append(cat_table)
                story.append(Spacer(1, 0.2*inch))
            
            story.append(PageBreak())
        
        # CORRELATION ANALYSIS
        if len(self.numeric_cols) >= 2:
            story.append(Paragraph("🔗 CORRELATION ANALYSIS", heading_style))
            story.append(Spacer(1, 0.1*inch))
            
            corr_matrix = self.df[self.numeric_cols[:6]].corr()
            
            # Create correlation table
            corr_data = [[''] + self.numeric_cols[:6]]
            for col in self.numeric_cols[:6]:
                row = [col]
                for col2 in self.numeric_cols[:6]:
                    corr_val = corr_matrix.loc[col, col2]
                    row.append(f"{corr_val:.3f}")
                corr_data.append(row)
            
            corr_table = Table(corr_data)
            corr_table.setStyle(self._get_correlation_table_style())
            story.append(corr_table)
            
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("<b>Strong Correlations (|r| > 0.7):</b>", styles['Normal']))
            
            strong_corr_data = [['Variable 1', 'Variable 2', 'Correlation', 'Interpretation']]
            for i in range(len(self.numeric_cols[:6])):
                for j in range(i+1, len(self.numeric_cols[:6])):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        interpretation = "Strong Positive" if corr_val > 0 else "Strong Negative"
                        strong_corr_data.append([
                            self.numeric_cols[i],
                            self.numeric_cols[j],
                            f"{corr_val:.3f}",
                            interpretation
                        ])
            
            if len(strong_corr_data) > 1:
                strong_corr_table = Table(strong_corr_data, colWidths=[2*inch, 2*inch, 1.5*inch, 2*inch])
                strong_corr_table.setStyle(self._get_highlight_table_style())
                story.append(strong_corr_table)
            else:
                story.append(Paragraph("No strong correlations found.", styles['Normal']))
            
            story.append(PageBreak())
        
        # DATA SAMPLE
        story.append(Paragraph("📄 DATA SAMPLE (First 20 Rows)", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        sample_data = [list(self.df.columns[:10])]  # Limit to 10 columns for space
        for idx, row in self.df.head(20).iterrows():
            sample_data.append([str(val)[:20] for val in row.values[:10]])
        
        sample_table = Table(sample_data)
        sample_table.setStyle(self._get_data_table_style())
        story.append(sample_table)
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def _get_date_range(self):
        """Get date range from datetime columns"""
        try:
            for col in self.df.columns:
                try:
                    dates = pd.to_datetime(self.df[col], errors='coerce').dropna()
                    if len(dates) > 0:
                        return f"{dates.min().strftime('%Y-%m-%d')} to {dates.max().strftime('%Y-%m-%d')}"
                except:
                    pass
        except:
            pass
        return "N/A"
    
    def _get_header_table_style(self):
        """Professional table style with header"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
    
    def _get_striped_table_style(self):
        """Striped table style"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f9ff')]),
        ])
    
    def _get_correlation_table_style(self):
        """Correlation matrix style"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1e3a8a')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ])
    
    def _get_highlight_table_style(self):
        """Highlighted table for important findings"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ])
    
    def _get_data_table_style(self):
        """Data sample table style"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#475569')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No filepath provided"}))
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    generator = DetailedReportGenerator(filepath)
    
    if not generator.load_data():
        print(json.dumps({"success": False, "error": "Failed to load data"}))
        sys.exit(1)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"Detailed_Analytics_Report_{timestamp}.pdf"
    
    output_path = generator.generate_pdf(output_filename)
    
    print(json.dumps({
        "success": True,
        "filename": output_filename,
        "path": output_path
    }))