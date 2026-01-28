#!/usr/bin/env python3
"""
Improved Autonomous AI - Better data preparation for visualizations
"""
import pandas as pd
import numpy as np
import json
import sys

class ImprovedAutonomousAI:
    def __init__(self):
        self.df = None
        self.filepath = None
        self.insights = []
        self.auto_visualizations = []
        self.toggles = []
        self.metadata = {}
        
    def load_data(self, filepath):
        """Load data"""
        try:
            self.filepath = filepath
            if filepath.endswith('.csv'):
                self.df = pd.read_csv(filepath, encoding='utf-8')
            else:
                self.df = pd.read_excel(filepath, engine='openpyxl')
            
            # Clean column names
            self.df.columns = [str(col).strip() for col in self.df.columns]
            
            return True
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return False
    
    def analyze_and_decide(self):
        """AI analyzes and creates visualizations"""
        self._analyze_columns()
        self._auto_select_visualizations()
        self._generate_toggles()
        self._generate_insights()
    
    def _analyze_columns(self):
        """Understand data structure"""
        for col in self.df.columns:
            col_type = self._detect_type(col)
            unique_count = self.df[col].nunique()
            missing_pct = (self.df[col].isna().sum() / len(self.df)) * 100
            
            self.metadata[col] = {
                'type': col_type,
                'unique_count': unique_count,
                'missing_pct': missing_pct,
                'sample_values': self.df[col].dropna().head(3).tolist()
            }
    
    def _detect_type(self, col):
        """Detect column type"""
        # Try numeric first
        try:
            pd.to_numeric(self.df[col], errors='raise')
            return 'numeric'
        except:
            pass
        
        # Try datetime
        try:
            pd.to_datetime(self.df[col], errors='raise')
            return 'datetime'
        except:
            pass
        
        # Categorical if low cardinality
        if self.df[col].nunique() / len(self.df) < 0.5 and self.df[col].nunique() < 50:
            return 'categorical'
        
        return 'text'
    
    def _auto_select_visualizations(self):
        """AI selects best visualizations WITH data preparation instructions"""
        numeric_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'numeric']
        categorical_cols = [col for col, meta in self.metadata.items() 
                          if meta['type'] == 'categorical' and meta['unique_count'] < 20]
        datetime_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'datetime']
        
        # 1. PIE CHARTS - Top categorical distributions
        for cat_col in categorical_cols[:3]:
            if self.metadata[cat_col]['unique_count'] <= 10:
                self.auto_visualizations.append({
                    'type': 'pie',
                    'title': f'Distribution of {cat_col}',
                    'category': cat_col,
                    'description': f'Shows the percentage breakdown of {cat_col}',
                    'priority': 'high',
                    'data_prep': 'value_counts'  # Instructions for data preparation
                })
        
        # 2. BAR CHARTS - For comparisons
        for cat_col in categorical_cols[:4]:
            self.auto_visualizations.append({
                'type': 'bar',
                'title': f'{cat_col} Frequency Analysis',
                'x': cat_col,
                'y': 'count',
                'description': f'Compare frequencies across {cat_col} categories',
                'priority': 'high',
                'data_prep': 'value_counts'
            })
        
        # 3. LINE CHARTS - Trends over time
        if datetime_cols and numeric_cols:
            for num_col in numeric_cols[:2]:
                self.auto_visualizations.append({
                    'type': 'line',
                    'title': f'{num_col} Over Time',
                    'x': datetime_cols[0],
                    'y': num_col,
                    'description': f'Time series trend of {num_col}',
                    'priority': 'high',
                    'data_prep': 'time_series'
                })
        
        # 4. SCATTER PLOTS - Correlations
        if len(numeric_cols) >= 2:
            self.auto_visualizations.append({
                'type': 'scatter',
                'title': f'{numeric_cols[0]} vs {numeric_cols[1]}',
                'x': numeric_cols[0],
                'y': numeric_cols[1],
                'description': f'Relationship between {numeric_cols[0]} and {numeric_cols[1]}',
                'priority': 'high',
                'data_prep': 'correlation'
            })
        
        # 5. HORIZONTAL BAR - Better for many categories
        for cat_col in categorical_cols[:2]:
            if self.metadata[cat_col]['unique_count'] > 5:
                self.auto_visualizations.append({
                    'type': 'horizontal_bar',
                    'title': f'{cat_col} Rankings',
                    'x': cat_col,
                    'y': 'count',
                    'description': f'Ranked horizontal view of {cat_col}',
                    'priority': 'medium',
                    'data_prep': 'value_counts_sorted'
                })
        
        # 6. AREA CHARTS - Cumulative trends
        if datetime_cols and numeric_cols:
            self.auto_visualizations.append({
                'type': 'area',
                'title': f'{numeric_cols[0]} Cumulative View',
                'x': datetime_cols[0],
                'y': numeric_cols[0],
                'description': f'Filled area showing {numeric_cols[0]} volume',
                'priority': 'medium',
                'data_prep': 'time_series'
            })
        
        # 7. MULTI-CATEGORY ANALYSIS
        if len(categorical_cols) >= 2 and numeric_cols:
            self.auto_visualizations.append({
                'type': 'stacked_bar',
                'title': f'{categorical_cols[0]} by {categorical_cols[1]}',
                'x': categorical_cols[0],
                'y': numeric_cols[0] if numeric_cols else 'count',
                'stack': categorical_cols[1],
                'description': f'Grouped analysis of {categorical_cols[0]} and {categorical_cols[1]}',
                'priority': 'medium',
                'data_prep': 'grouped'
            })
    
    def _generate_toggles(self):
        """Generate smart filters"""
        categorical_cols = [col for col, meta in self.metadata.items() 
                          if meta['type'] == 'categorical' and meta['unique_count'] < 20]
        numeric_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'numeric']
        
        # Category filters
        for cat_col in categorical_cols[:3]:
            unique_values = self.df[cat_col].dropna().unique().tolist()
            self.toggles.append({
                'type': 'multi_select',
                'label': f'Filter by {cat_col}',
                'column': cat_col,
                'options': [str(v) for v in unique_values][:20],
                'description': f'Select specific {cat_col} values'
            })
        
        # Range sliders
        for num_col in numeric_cols[:2]:
            min_val = float(self.df[num_col].min())
            max_val = float(self.df[num_col].max())
            self.toggles.append({
                'type': 'range_slider',
                'label': f'{num_col} Range',
                'column': num_col,
                'min': min_val,
                'max': max_val,
                'description': f'Filter by {num_col} value range'
            })
    
    def _generate_insights(self):
        """Generate insights"""
        self.insights.append(f"✅ Dataset: {len(self.df):,} rows × {len(self.df.columns)} columns")
        self.insights.append(f"📊 AI selected {len(self.auto_visualizations)} optimal visualizations")
        self.insights.append(f"🎛️ {len(self.toggles)} interactive filters available")
        
        # Data quality
        missing = self.df.isnull().sum().sum()
        if missing == 0:
            self.insights.append("✨ Perfect data quality - no missing values")
        else:
            self.insights.append(f"⚠️ {missing:,} missing values detected")
        
        # Top insights
        numeric_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'numeric']
        for num_col in numeric_cols[:2]:
            mean_val = self.df[num_col].mean()
            self.insights.append(f"📈 Average {num_col}: {mean_val:,.2f}")
    
    def prepare_visualization_data(self, viz_config):
        """Prepare data for specific visualization"""
        try:
            viz_type = viz_config.get('type')
            data_prep = viz_config.get('data_prep', 'basic')
            
            if data_prep == 'value_counts':
                # For pie/bar charts
                col = viz_config.get('category') or viz_config.get('x')
                if col and col in self.df.columns:
                    value_counts = self.df[col].value_counts().head(10)
                    data = [
                        {'category': str(idx), 'value': int(val), 'count': int(val)}
                        for idx, val in value_counts.items()
                    ]
                    return data
            
            elif data_prep == 'value_counts_sorted':
                # Sorted value counts
                col = viz_config.get('x')
                if col and col in self.df.columns:
                    value_counts = self.df[col].value_counts().sort_values(ascending=False).head(15)
                    data = [
                        {viz_config.get('x'): str(idx), 'count': int(val)}
                        for idx, val in value_counts.items()
                    ]
                    return data
            
            elif data_prep == 'time_series':
                # For line/area charts
                x_col = viz_config.get('x')
                y_col = viz_config.get('y')
                
                if x_col in self.df.columns and y_col in self.df.columns:
                    df_clean = self.df[[x_col, y_col]].dropna()
                    df_clean[x_col] = pd.to_datetime(df_clean[x_col], errors='coerce')
                    df_clean = df_clean.dropna()
                    df_clean = df_clean.sort_values(x_col)
                    
                    # Group by date
                    df_grouped = df_clean.groupby(x_col)[y_col].mean().reset_index()
                    
                    data = [
                        {x_col: str(row[x_col]), y_col: float(row[y_col])}
                        for _, row in df_grouped.head(100).iterrows()
                    ]
                    return data
            
            elif data_prep == 'correlation':
                # For scatter plots
                x_col = viz_config.get('x')
                y_col = viz_config.get('y')
                
                if x_col in self.df.columns and y_col in self.df.columns:
                    df_clean = self.df[[x_col, y_col]].dropna()
                    df_clean[x_col] = pd.to_numeric(df_clean[x_col], errors='coerce')
                    df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
                    df_clean = df_clean.dropna()
                    
                    data = [
                        {x_col: float(row[x_col]), y_col: float(row[y_col])}
                        for _, row in df_clean.head(500).iterrows()
                    ]
                    return data
            
            # Default: return first 100 rows
            return self.df.head(100).to_dict('records')
            
        except Exception as e:
            print(f"Error preparing data: {str(e)}", file=sys.stderr)
            return []
    
    def get_results(self):
        """Return results"""
        return {
            'success': True,
            'visualizations': self.auto_visualizations,
            'toggles': self.toggles,
            'insights': self.insights,
            'metadata': {col: {k: v for k, v in meta.items() if k != 'sample_values'} 
                        for col, meta in self.metadata.items()},
            'summary': {
                'total_rows': len(self.df),
                'total_columns': len(self.df.columns),
                'columns': list(self.df.columns)
            }
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No filepath provided"}))
        sys.exit(1)
    
    filepath = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'analyze'
    
    ai = ImprovedAutonomousAI()
    
    if not ai.load_data(filepath):
        print(json.dumps({"success": False, "error": "Failed to load data"}))
        sys.exit(1)
    
    if command == 'analyze':
        ai.analyze_and_decide()
        results = ai.get_results()
        print(json.dumps(results))
    
    elif command == 'prepare_viz':
        # Get viz config from third argument
        viz_config = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        ai.analyze_and_decide()
        data = ai.prepare_visualization_data(viz_config)
        print(json.dumps({'success': True, 'data': data}))