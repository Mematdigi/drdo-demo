#!/usr/bin/env python3
"""
Smart Analytics Report Generator
- Analyzes trends in data
- Makes predictions
- Provides insights and recommendations
"""
import json
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from scipy import stats
from sklearn.linear_model import LinearRegression

class SmartReportGenerator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.insights = []
        self.predictions = []
        self.trends = []
        self.recommendations = []
        
    def load_and_analyze(self):
        """Load data and perform comprehensive analysis"""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            else:
                self.df = pd.read_excel(self.filepath)
            
            # Perform analyses
            self.analyze_trends()
            self.detect_patterns()
            self.make_predictions()
            self.generate_insights()
            self.generate_recommendations()
            
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def analyze_trends(self):
        """Analyze trends in numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if self.df[col].notna().sum() > 5:  # Need at least 5 data points
                values = self.df[col].dropna()
                
                # Calculate trend
                x = np.arange(len(values))
                y = values.values
                
                if len(x) > 1:
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                    
                    trend_direction = "increasing" if slope > 0 else "decreasing"
                    strength = "strong" if abs(r_value) > 0.7 else "moderate" if abs(r_value) > 0.4 else "weak"
                    
                    self.trends.append({
                        'column': col,
                        'direction': trend_direction,
                        'strength': strength,
                        'slope': slope,
                        'r_squared': r_value ** 2,
                        'mean': values.mean(),
                        'std': values.std(),
                        'min': values.min(),
                        'max': values.max()
                    })
    
    def detect_patterns(self):
        """Detect patterns and anomalies"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            values = self.df[col].dropna()
            
            if len(values) > 10:
                # Detect outliers
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                outliers = values[(values < Q1 - 1.5 * IQR) | (values > Q3 + 1.5 * IQR)]
                
                if len(outliers) > 0:
                    self.insights.append({
                        'type': 'outlier',
                        'column': col,
                        'message': f"Found {len(outliers)} outlier(s) in {col}",
                        'detail': f"Range: {outliers.min():.2f} to {outliers.max():.2f}"
                    })
                
                # Check for seasonality (if enough data)
                if len(values) > 30:
                    # Simple seasonality check
                    autocorr = pd.Series(values.values).autocorr(lag=7)
                    if abs(autocorr) > 0.5:
                        self.insights.append({
                            'type': 'pattern',
                            'column': col,
                            'message': f"Detected cyclical pattern in {col}",
                            'detail': f"7-day autocorrelation: {autocorr:.2f}"
                        })
    
    def make_predictions(self):
        """Make future predictions based on trends"""
        for trend in self.trends:
            col = trend['column']
            
            if trend['strength'] in ['strong', 'moderate']:
                # Simple linear prediction
                current_value = trend['mean']
                predicted_change = trend['slope'] * 10  # Predict 10 steps ahead
                predicted_value = current_value + predicted_change
                
                change_pct = (predicted_change / current_value * 100) if current_value != 0 else 0
                
                self.predictions.append({
                    'column': col,
                    'current_value': current_value,
                    'predicted_value': predicted_value,
                    'change': predicted_change,
                    'change_percent': change_pct,
                    'confidence': trend['strength'],
                    'direction': trend['direction']
                })
    
    def generate_insights(self):
        """Generate key insights from data"""
        
        # Correlation insights
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            
            # Find strong correlations
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    
                    if abs(corr_value) > 0.7:
                        col1 = corr_matrix.columns[i]
                        col2 = corr_matrix.columns[j]
                        
                        relationship = "positively" if corr_value > 0 else "negatively"
                        
                        self.insights.append({
                            'type': 'correlation',
                            'column': f"{col1} & {col2}",
                            'message': f"{col1} and {col2} are {relationship} correlated",
                            'detail': f"Correlation coefficient: {corr_value:.2f}"
                        })
        
        # Distribution insights
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            values = self.df[col].dropna()
            
            if len(values) > 5:
                skewness = values.skew()
                
                if abs(skewness) > 1:
                    direction = "right" if skewness > 0 else "left"
                    self.insights.append({
                        'type': 'distribution',
                        'column': col,
                        'message': f"{col} shows {direction}-skewed distribution",
                        'detail': f"Skewness: {skewness:.2f}"
                    })
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        
        # Based on trends
        for trend in self.trends:
            if trend['strength'] == 'strong':
                if trend['direction'] == 'increasing':
                    self.recommendations.append({
                        'priority': 'High',
                        'category': 'Growth Opportunity',
                        'recommendation': f"Capitalize on increasing trend in {trend['column']}",
                        'action': f"Current growth rate suggests {trend['column']} will continue to rise. Consider allocating more resources to this area."
                    })
                else:
                    self.recommendations.append({
                        'priority': 'High',
                        'category': 'Risk Alert',
                        'recommendation': f"Address declining trend in {trend['column']}",
                        'action': f"Declining pattern detected. Investigate root causes and implement corrective measures."
                    })
        
        # Based on predictions
        for pred in self.predictions:
            if abs(pred['change_percent']) > 20:
                self.recommendations.append({
                    'priority': 'Medium',
                    'category': 'Forecast',
                    'recommendation': f"Prepare for significant change in {pred['column']}",
                    'action': f"Expected {pred['change_percent']:.1f}% {'increase' if pred['change_percent'] > 0 else 'decrease'}. Plan accordingly."
                })
        
        # Data quality recommendations
        missing_data = self.df.isnull().sum()
        high_missing = missing_data[missing_data > len(self.df) * 0.1]
        
        if len(high_missing) > 0:
            self.recommendations.append({
                'priority': 'Medium',
                'category': 'Data Quality',
                'recommendation': 'Improve data collection for columns with high missing values',
                'action': f"Columns {', '.join(high_missing.index[:3])} have >10% missing data. Improve data collection processes."
            })
    
    def generate_pdf(self, output_filename):
        """Generate comprehensive PDF report"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(script_dir, '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        output_path = os.path.join(reports_dir, output_filename)
        
        doc = SimpleDocTemplate(output_path, pagesize=landscape(letter),
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=10,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Cover Page
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph("📊 Smart Analytics Report", title_style))
        story.append(Paragraph("AI-Powered Data Analysis with Predictions & Insights", subtitle_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              styles['Normal']))
        story.append(Paragraph(f"Dataset: {len(self.df)} rows × {len(self.df.columns)} columns", 
                              styles['Normal']))
        story.append(PageBreak())
        
        # Executive Summary
        story.append(Paragraph("📋 Executive Summary", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        
        summary_text = f"""
        This report provides comprehensive analysis of your dataset containing {len(self.df):,} records 
        across {len(self.df.columns)} variables. Our AI-powered analysis has identified {len(self.trends)} 
        significant trends, {len(self.insights)} key insights, and generated {len(self.predictions)} 
        predictions about future patterns. Based on this analysis, we provide {len(self.recommendations)} 
        actionable recommendations to optimize your outcomes.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(PageBreak())
        
        # Trend Analysis
        if self.trends:
            story.append(Paragraph("📈 Trend Analysis", styles['Heading1']))
            story.append(Spacer(1, 0.2*inch))
            
            trend_data = [['Metric', 'Trend Direction', 'Strength', 'Current Average', 'Growth Rate']]
            
            for trend in self.trends:
                trend_data.append([
                    trend['column'],
                    trend['direction'].title(),
                    trend['strength'].title(),
                    f"{trend['mean']:.2f}",
                    f"{trend['slope']:.2f}/period"
                ])
            
            trend_table = Table(trend_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            trend_table.setStyle(self._get_table_style())
            story.append(trend_table)
            story.append(PageBreak())
        
        # Predictions
        if self.predictions:
            story.append(Paragraph("🔮 Predictions & Forecasts", styles['Heading1']))
            story.append(Spacer(1, 0.2*inch))
            
            pred_data = [['Metric', 'Current Value', 'Predicted Value', 'Expected Change', 'Confidence']]
            
            for pred in self.predictions:
                arrow = "↗" if pred['change_percent'] > 0 else "↘"
                pred_data.append([
                    pred['column'],
                    f"{pred['current_value']:.2f}",
                    f"{pred['predicted_value']:.2f}",
                    f"{arrow} {abs(pred['change_percent']):.1f}%",
                    pred['confidence'].title()
                ])
            
            pred_table = Table(pred_data, colWidths=[2*inch, 1.8*inch, 1.8*inch, 1.8*inch, 1.5*inch])
            pred_table.setStyle(self._get_table_style())
            story.append(pred_table)
            
            story.append(Spacer(1, 0.3*inch))
            story.append(Paragraph("<b>Interpretation:</b> These predictions are based on historical trends. "
                                 "Strong confidence indicates reliable patterns, while moderate confidence "
                                 "suggests higher variability.", styles['Normal']))
            story.append(PageBreak())
        
        # Key Insights
        if self.insights:
            story.append(Paragraph("💡 Key Insights", styles['Heading1']))
            story.append(Spacer(1, 0.2*inch))
            
            for idx, insight in enumerate(self.insights, 1):
                insight_style = ParagraphStyle(
                    'Insight',
                    parent=styles['Normal'],
                    leftIndent=20,
                    spaceAfter=10
                )
                
                icon = "🔍" if insight['type'] == 'outlier' else "📊" if insight['type'] == 'correlation' else "🔄"
                
                story.append(Paragraph(f"<b>{icon} Insight {idx}: {insight['message']}</b>", styles['Normal']))
                story.append(Paragraph(insight['detail'], insight_style))
            
            story.append(PageBreak())
        
        # Recommendations
        if self.recommendations:
            story.append(Paragraph("✅ Actionable Recommendations", styles['Heading1']))
            story.append(Spacer(1, 0.2*inch))
            
            rec_data = [['Priority', 'Category', 'Recommendation', 'Action Steps']]
            
            for rec in self.recommendations:
                priority_color = colors.red if rec['priority'] == 'High' else colors.orange
                rec_data.append([
                    rec['priority'],
                    rec['category'],
                    rec['recommendation'],
                    rec['action']
                ])
            
            rec_table = Table(rec_data, colWidths=[1*inch, 1.5*inch, 2.5*inch, 3.5*inch])
            rec_table.setStyle(self._get_table_style())
            story.append(rec_table)
            story.append(PageBreak())
        
        # Data Overview
        story.append(Paragraph("📊 Data Overview", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        
        overview_data = [['Metric', 'Value']]
        overview_data.append(['Total Records', f"{len(self.df):,}"])
        overview_data.append(['Total Variables', str(len(self.df.columns))])
        overview_data.append(['Numeric Variables', str(len(self.df.select_dtypes(include=[np.number]).columns))])
        overview_data.append(['Date/Time Variables', str(len(self.df.select_dtypes(include=['datetime64']).columns))])
        overview_data.append(['Text Variables', str(len(self.df.select_dtypes(include=['object']).columns))])
        overview_data.append(['Missing Values', f"{self.df.isnull().sum().sum():,}"])
        overview_data.append(['Completeness', f"{(1 - self.df.isnull().sum().sum()/(len(self.df)*len(self.df.columns)))*100:.1f}%"])
        
        overview_table = Table(overview_data, colWidths=[3*inch, 2*inch])
        overview_table.setStyle(self._get_table_style())
        story.append(overview_table)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("This report was generated by Smart Data Studio's AI Analytics Engine", footer_style))
        story.append(Paragraph("For questions or deeper analysis, consult with your data team", footer_style))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _get_table_style(self):
        """Standard table style"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print(json.dumps({"success": False, "error": "Usage: python smart_analytics_report.py <filepath>"}))
            sys.exit(1)
        
        filepath = sys.argv[1]
        
        generator = SmartReportGenerator(filepath)
        
        if not generator.load_and_analyze():
            print(json.dumps({"success": False, "error": "Failed to load and analyze data"}))
            sys.exit(1)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"Smart_Analytics_{timestamp}.pdf"
        
        output_path = generator.generate_pdf(output_filename)
        
        print(json.dumps({
            "success": True,
            "filename": output_filename,
            "path": output_path,
            "insights_count": len(generator.insights),
            "predictions_count": len(generator.predictions),
            "recommendations_count": len(generator.recommendations)
        }))
        
    except Exception as e:
        import traceback
        print(json.dumps({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }))
        sys.exit(1)