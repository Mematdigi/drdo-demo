#!/usr/bin/env python3
"""
Enhanced Autonomous AI - Generates 15+ visualizations
"""
import pandas as pd
import numpy as np
import json
import sys

class EnhancedAutonomousAI:
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
            
            self.df.columns = [str(col).strip() for col in self.df.columns]
            return True
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return False
    
    def analyze_and_decide(self):
        """AI analyzes and creates ALL visualizations"""
        self._analyze_columns()
        self._auto_select_ALL_visualizations()
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
                'missing_pct': missing_pct
            }
    
    def _detect_type(self, col):
        """Detect column type"""
        try:
            pd.to_numeric(self.df[col], errors='raise')
            return 'numeric'
        except:
            pass
        
        try:
            pd.to_datetime(self.df[col], errors='raise')
            return 'datetime'
        except:
            pass
        
        if self.df[col].nunique() / len(self.df) < 0.5 and self.df[col].nunique() < 50:
            return 'categorical'
        
        return 'text'
    
    def _auto_select_ALL_visualizations(self):
        """Generate ALL 15+ visualization types"""
        
        numeric_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'numeric']
        categorical_cols = [col for col, meta in self.metadata.items() 
                          if meta['type'] == 'categorical' and meta['unique_count'] < 30]
        datetime_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'datetime']
        
        # 1-3. PIE & DONUT CHARTS (multiple)
        for idx, cat_col in enumerate(categorical_cols[:3]):
            if self.metadata[cat_col]['unique_count'] <= 10:
                chart_type = 'donut' if idx % 2 == 0 else 'pie'
                self.auto_visualizations.append({
                    'type': chart_type,
                    'title': f'Distribution of {cat_col}',
                    'category': cat_col,
                    'description': f'Percentage breakdown of {cat_col}',
                    'priority': 'high',
                    'data_prep': 'value_counts'
                })
        
        # 4-6. BAR CHARTS (vertical)
        for cat_col in categorical_cols[:3]:
            self.auto_visualizations.append({
                'type': 'bar',
                'title': f'{cat_col} Frequency',
                'x': cat_col,
                'y': 'count',
                'description': f'Bar chart showing {cat_col} counts',
                'priority': 'high',
                'data_prep': 'value_counts'
            })
        
        # 7-8. HORIZONTAL BAR CHARTS
        for cat_col in categorical_cols[:2]:
            if self.metadata[cat_col]['unique_count'] > 5:
                self.auto_visualizations.append({
                    'type': 'horizontal_bar',
                    'title': f'{cat_col} Rankings',
                    'x': cat_col,
                    'y': 'count',
                    'description': f'Horizontal ranking of {cat_col}',
                    'priority': 'medium',
                    'data_prep': 'value_counts_sorted'
                })
        
        # 9-11. LINE CHARTS
        if datetime_cols and numeric_cols:
            for num_col in numeric_cols[:3]:
                self.auto_visualizations.append({
                    'type': 'line',
                    'title': f'{num_col} Over Time',
                    'x': datetime_cols[0],
                    'y': num_col,
                    'description': f'Time series trend of {num_col}',
                    'priority': 'high',
                    'data_prep': 'time_series',
                    'smooth': True
                })
        
        # 12-13. AREA CHARTS
        if datetime_cols and numeric_cols:
            for num_col in numeric_cols[:2]:
                self.auto_visualizations.append({
                    'type': 'area',
                    'title': f'{num_col} Volume',
                    'x': datetime_cols[0],
                    'y': num_col,
                    'description': f'Cumulative view of {num_col}',
                    'priority': 'medium',
                    'data_prep': 'time_series'
                })
        
        # 14-16. SCATTER PLOTS
        if len(numeric_cols) >= 2:
            for i in range(min(3, len(numeric_cols))):
                for j in range(i+1, min(i+2, len(numeric_cols))):
                    self.auto_visualizations.append({
                        'type': 'scatter',
                        'title': f'{numeric_cols[i]} vs {numeric_cols[j]}',
                        'x': numeric_cols[i],
                        'y': numeric_cols[j],
                        'description': f'Correlation analysis',
                        'priority': 'medium',
                        'data_prep': 'correlation'
                    })
        
        # 17. BUBBLE CHART
        if len(numeric_cols) >= 3 and categorical_cols:
            self.auto_visualizations.append({
                'type': 'bubble',
                'title': 'Multi-Dimensional Analysis',
                'x': numeric_cols[0],
                'y': numeric_cols[1],
                'size': numeric_cols[2],
                'color': categorical_cols[0],
                'description': '4D bubble visualization',
                'priority': 'high',
                'data_prep': 'bubble'
            })
        
        # 18. STACKED BAR
        if len(categorical_cols) >= 2:
            self.auto_visualizations.append({
                'type': 'stacked_bar',
                'title': f'{categorical_cols[0]} by {categorical_cols[1]}',
                'x': categorical_cols[0],
                'stack': categorical_cols[1],
                'description': 'Grouped category analysis',
                'priority': 'high',
                'data_prep': 'stacked'
            })
        
        # 19. GANTT CHART (if 2+ datetime columns OR create synthetic)
        if len(datetime_cols) >= 2:
            self.auto_visualizations.append({
                'type': 'gantt',
                'title': 'Timeline Gantt Chart',
                'start': datetime_cols[0],
                'end': datetime_cols[1],
                'task': categorical_cols[0] if categorical_cols else self.df.columns[0],
                'description': 'Timeline with start/end dates',
                'priority': 'high',
                'data_prep': 'gantt'
            })
        elif datetime_cols and categorical_cols:
            # Create synthetic Gantt
            self.auto_visualizations.append({
                'type': 'gantt',
                'title': 'Synthetic Timeline',
                'start': datetime_cols[0],
                'task': categorical_cols[0],
                'description': 'Timeline view (synthetic duration)',
                'priority': 'medium',
                'data_prep': 'gantt_synthetic'
            })
        
        # 20. HEATMAP
        if len(numeric_cols) >= 3:
            self.auto_visualizations.append({
                'type': 'heatmap',
                'title': 'Correlation Heatmap',
                'columns': numeric_cols[:10],
                'description': 'Variable correlation matrix',
                'priority': 'medium',
                'data_prep': 'heatmap'
            })
        
        # 21-22. BOX PLOTS
        for num_col in numeric_cols[:2]:
            if categorical_cols:
                self.auto_visualizations.append({
                    'type': 'box',
                    'title': f'{num_col} Distribution by {categorical_cols[0]}',
                    'y': num_col,
                    'group': categorical_cols[0],
                    'description': 'Statistical box plot',
                    'priority': 'low',
                    'data_prep': 'box'
                })
        
        # 23. RADAR CHART
        if len(numeric_cols) >= 3 and categorical_cols:
            self.auto_visualizations.append({
                'type': 'radar',
                'title': 'Multi-Metric Radar',
                'metrics': numeric_cols[:6],
                'category': categorical_cols[0],
                'description': 'Spider web comparison',
                'priority': 'medium',
                'data_prep': 'radar'
            })
        
        # 24. TREEMAP
        if len(categorical_cols) >= 2:
            self.auto_visualizations.append({
                'type': 'treemap',
                'title': 'Hierarchical Treemap',
                'category1': categorical_cols[0],
                'category2': categorical_cols[1],
                'value': numeric_cols[0] if numeric_cols else 'count',
                'description': 'Nested visualization',
                'priority': 'low',
                'data_prep': 'treemap'
            })
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        self.auto_visualizations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        print(f"Generated {len(self.auto_visualizations)} visualizations", file=sys.stderr)
    
    def _generate_toggles(self):
        """Generate smart filters INCLUDING DATA RANGE"""
        
        categorical_cols = [col for col, meta in self.metadata.items() 
                          if meta['type'] == 'categorical' and meta['unique_count'] < 20]
        numeric_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'numeric']
        datetime_cols = [col for col, meta in self.metadata.items() if meta['type'] == 'datetime']
        
        # DATA RANGE SELECTOR (start/end row)
        self.toggles.append({
            'type': 'data_range',
            'label': 'Select Data Range (Rows)',
            'min': 0,
            'max': len(self.df) - 1,
            'default': [0, min(100, len(self.df) - 1)],
            'description': 'Choose which rows to visualize'
        })
        
        # Category filters
        for cat_col in categorical_cols[:3]:
            unique_values = self.df[cat_col].dropna().unique().tolist()[:20]
            self.toggles.append({
                'type': 'multi_select',
                'label': f'Filter by {cat_col}',
                'column': cat_col,
                'options': [str(v) for v in unique_values],
                'description': f'Select {cat_col} values'
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
                'default': [min_val, max_val],
                'description': f'Filter {num_col} values'
            })
        
        # Date range
        for dt_col in datetime_cols[:1]:
            self.toggles.append({
                'type': 'date_range',
                'label': 'Date Range',
                'column': dt_col,
                'description': 'Filter by date'
            })
    
    def _generate_insights(self):
        """Generate insights"""
        self.insights.append(f"✅ Dataset: {len(self.df):,} rows × {len(self.df.columns)} columns")
        self.insights.append(f"📊 AI generated {len(self.auto_visualizations)} visualizations automatically")
        self.insights.append(f"🎛️ {len(self.toggles)} interactive filters available")
        
        missing = self.df.isnull().sum().sum()
        if missing == 0:
            self.insights.append("✨ Perfect data quality")
        else:
            self.insights.append(f"⚠️ {missing:,} missing values")
    
    def get_results(self):
        """Return results"""
        return {
            'success': True,
            'visualizations': self.auto_visualizations,
            'toggles': self.toggles,
            'insights': self.insights,
            'metadata': {col: {k: v for k, v in meta.items()} 
                        for col, meta in self.metadata.items()},
            'summary': {
                'total_rows': len(self.df),
                'total_columns': len(self.df.columns),
                'columns': list(self.df.columns)
            }
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No filepath"}))
        sys.exit(1)
    
    filepath = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'analyze'
    
    ai = EnhancedAutonomousAI()
    
    if not ai.load_data(filepath):
        print(json.dumps({"success": False, "error": "Failed to load"}))
        sys.exit(1)
    
    if command == 'analyze':
        ai.analyze_and_decide()
        results = ai.get_results()
        print(json.dumps(results))