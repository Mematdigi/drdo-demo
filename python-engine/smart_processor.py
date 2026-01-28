#!/usr/bin/env python3
"""
Smart Data Processor - Works with ANY data format
Auto-detects columns, cleans data, prepares for visualization
"""
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import re

class SmartDataProcessor:
    def __init__(self):
        self.df = None
        self.metadata = {}
        self.cleaning_report = []
        
    def load_data(self, filepath):
        """Load data from CSV or Excel - auto-detect format"""
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                self.cleaning_report.append(f"❌ File not found: {filepath}")
                return False
            
            if filepath.endswith('.csv'):
                self.df = pd.read_csv(filepath)
                self.cleaning_report.append(f"✅ Loaded CSV file")
            elif filepath.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(filepath)
                self.cleaning_report.append(f"✅ Loaded Excel file")
            else:
                self.cleaning_report.append(f"❌ Unsupported file format")
                return False
            
            if self.df is not None and not self.df.empty:
                self.cleaning_report.append(f"✅ Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
                return True
            else:
                self.cleaning_report.append(f"❌ File is empty")
                return False
                
        except Exception as e:
            self.cleaning_report.append(f"❌ Load error: {str(e)}")
            return False
    
    def analyze_columns(self):
        """Auto-detect column types and characteristics"""
        if self.df is None:
            return {}
        
        column_info = {}
        
        for col in self.df.columns:
            info = {
                'name': col,
                'original_type': str(self.df[col].dtype),
                'missing_count': int(self.df[col].isna().sum()),
                'missing_percent': float(self.df[col].isna().sum() / len(self.df) * 100),
                'unique_count': int(self.df[col].nunique()),
                'sample_values': [str(v) for v in self.df[col].dropna().head(5).tolist()]  # Convert to string
            }
            
            # Detect actual data type
            info['detected_type'] = self._detect_column_type(self.df[col])
            
            # Add statistics based on type
            if info['detected_type'] == 'numeric':
                try:
                    info['min'] = float(self.df[col].min()) if not pd.isna(self.df[col].min()) else None
                    info['max'] = float(self.df[col].max()) if not pd.isna(self.df[col].max()) else None
                    info['mean'] = float(self.df[col].mean()) if not pd.isna(self.df[col].mean()) else None
                    info['median'] = float(self.df[col].median()) if not pd.isna(self.df[col].median()) else None
                except:
                    pass
            
            elif info['detected_type'] == 'categorical':
                try:
                    value_counts = self.df[col].value_counts().head(10)
                    info['top_values'] = {str(k): int(v) for k, v in value_counts.to_dict().items()}
                except:
                    info['top_values'] = {}
            
            elif info['detected_type'] == 'datetime':
                try:
                    min_val = self.df[col].min()
                    max_val = self.df[col].max()
                    info['min_date'] = str(min_val) if not pd.isna(min_val) else None
                    info['max_date'] = str(max_val) if not pd.isna(max_val) else None
                except:
                    info['min_date'] = None
                    info['max_date'] = None
            
            column_info[col] = info
        
        self.metadata['columns'] = column_info
        return column_info
    
    def _detect_column_type(self, series):
        """Detect the actual type of a column"""
        # Remove nulls for analysis
        series_clean = series.dropna()
        
        if len(series_clean) == 0:
            return 'unknown'
        
        # Check if numeric
        try:
            pd.to_numeric(series_clean, errors='raise')
            return 'numeric'
        except:
            pass
        
        # Check if datetime (suppress warnings)
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                pd.to_datetime(series_clean, errors='raise')
            return 'datetime'
        except:
            pass
        
        # Check if boolean
        try:
            unique_vals = series_clean.unique()
            if len(unique_vals) <= 2 and all(str(v).lower() in ['true', 'false', 'yes', 'no', '1', '0', 't', 'f', 'y', 'n'] for v in unique_vals):
                return 'boolean'
        except:
            pass
        
        # Check if categorical (low cardinality)
        try:
            if series_clean.nunique() / len(series_clean) < 0.5:
                return 'categorical'
        except:
            pass
        
        # Default to text
        return 'text'
    
    def clean_data(self, options=None):
        """Clean data based on detected issues"""
        if options is None:
            options = {
                'remove_duplicates': True,
                'handle_missing': 'smart',  # 'smart', 'drop', 'fill'
                'standardize_text': True,
                'convert_types': True,
                'remove_outliers': False
            }
        
        original_rows = len(self.df)
        
        # 1. Remove duplicates
        if options.get('remove_duplicates', True):
            before = len(self.df)
            self.df = self.df.drop_duplicates()
            removed = before - len(self.df)
            if removed > 0:
                self.cleaning_report.append(f"🧹 Removed {removed} duplicate rows")
        
        # 2. Handle missing values
        if options.get('handle_missing') == 'smart':
            for col in self.df.columns:
                col_type = self.metadata['columns'][col]['detected_type']
                missing_pct = self.metadata['columns'][col]['missing_percent']
                
                if missing_pct > 50:
                    # Too many missing - consider dropping column
                    self.cleaning_report.append(f"⚠️ Column '{col}' has {missing_pct:.1f}% missing values")
                
                elif missing_pct > 0:
                    if col_type == 'numeric':
                        # Fill with median
                        self.df[col].fillna(self.df[col].median(), inplace=True)
                        self.cleaning_report.append(f"🔧 Filled {col} missing values with median")
                    
                    elif col_type == 'categorical':
                        # Fill with mode
                        self.df[col].fillna(self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'Unknown', inplace=True)
                        self.cleaning_report.append(f"🔧 Filled {col} missing values with mode")
                    
                    else:
                        # Fill with 'Unknown' or 'N/A'
                        self.df[col].fillna('N/A', inplace=True)
                        self.cleaning_report.append(f"🔧 Filled {col} missing values with N/A")
        
        # 3. Convert data types
        if options.get('convert_types', True):
            import warnings
            for col in self.df.columns:
                col_type = self.metadata['columns'][col]['detected_type']
                
                try:
                    if col_type == 'numeric':
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    
                    elif col_type == 'datetime':
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    
                    elif col_type == 'boolean':
                        self.df[col] = self.df[col].map(lambda x: str(x).lower() in ['true', 'yes', '1', 't', 'y'])
                    
                    self.cleaning_report.append(f"✅ Converted {col} to {col_type}")
                
                except Exception as e:
                    self.cleaning_report.append(f"⚠️ Could not convert {col}: {str(e)}")
        
        # 4. Standardize text columns
        if options.get('standardize_text', True):
            for col in self.df.columns:
                if self.metadata['columns'][col]['detected_type'] in ['text', 'categorical']:
                    # Strip whitespace
                    self.df[col] = self.df[col].astype(str).str.strip()
                    # Standardize case for categorical
                    if self.metadata['columns'][col]['detected_type'] == 'categorical':
                        self.df[col] = self.df[col].str.title()
        
        # 5. Remove outliers (optional)
        if options.get('remove_outliers', False):
            for col in self.df.columns:
                if self.metadata['columns'][col]['detected_type'] == 'numeric':
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    
                    before = len(self.df)
                    self.df = self.df[(self.df[col] >= lower) & (self.df[col] <= upper)]
                    removed = before - len(self.df)
                    
                    if removed > 0:
                        self.cleaning_report.append(f"🎯 Removed {removed} outliers from {col}")
        
        final_rows = len(self.df)
        self.cleaning_report.append(f"📊 Final dataset: {final_rows} rows ({original_rows - final_rows} removed)")
        
        return self.cleaning_report
    
    def get_visualization_suggestions(self):
        """Suggest appropriate visualizations based on data"""
        suggestions = []
        
        numeric_cols = [col for col, info in self.metadata['columns'].items() 
                       if info['detected_type'] == 'numeric']
        categorical_cols = [col for col, info in self.metadata['columns'].items() 
                           if info['detected_type'] == 'categorical']
        datetime_cols = [col for col, info in self.metadata['columns'].items() 
                        if info['detected_type'] == 'datetime']
        
        # Bar charts for categorical
        for cat_col in categorical_cols:
            if self.metadata['columns'][cat_col]['unique_count'] <= 20:
                suggestions.append({
                    'type': 'bar',
                    'title': f'Distribution of {cat_col}',
                    'x': cat_col,
                    'y': 'count',
                    'description': f'Shows frequency of each category in {cat_col}'
                })
        
        # Histograms for numeric
        for num_col in numeric_cols:
            suggestions.append({
                'type': 'histogram',
                'title': f'Distribution of {num_col}',
                'x': num_col,
                'description': f'Shows the distribution pattern of {num_col}'
            })
        
        # Scatter plots for numeric pairs
        if len(numeric_cols) >= 2:
            for i in range(min(3, len(numeric_cols))):
                for j in range(i+1, min(3, len(numeric_cols))):
                    suggestions.append({
                        'type': 'scatter',
                        'title': f'{numeric_cols[i]} vs {numeric_cols[j]}',
                        'x': numeric_cols[i],
                        'y': numeric_cols[j],
                        'description': f'Shows relationship between {numeric_cols[i]} and {numeric_cols[j]}'
                    })
        
        # Line charts for time series
        if datetime_cols and numeric_cols:
            for dt_col in datetime_cols[:1]:
                for num_col in numeric_cols[:2]:
                    suggestions.append({
                        'type': 'line',
                        'title': f'{num_col} over Time',
                        'x': dt_col,
                        'y': num_col,
                        'description': f'Shows how {num_col} changes over time'
                    })
        
        # Pie charts for categorical with few categories
        for cat_col in categorical_cols:
            if 2 <= self.metadata['columns'][cat_col]['unique_count'] <= 8:
                suggestions.append({
                    'type': 'pie',
                    'title': f'{cat_col} Breakdown',
                    'category': cat_col,
                    'description': f'Shows proportion of each {cat_col}'
                })
        
        # Heatmap for numeric correlations
        if len(numeric_cols) >= 2:
            suggestions.append({
                'type': 'heatmap',
                'title': 'Correlation Matrix',
                'columns': numeric_cols[:10],
                'description': 'Shows correlations between numeric variables'
            })
        
        return suggestions
    
    def prepare_visualization_data(self, viz_config):
        """Prepare data for a specific visualization"""
        try:
            viz_type = viz_config.get('type')
            
            if not viz_type:
                return {'error': 'No visualization type specified'}
            
            def make_json_safe(data):
                """Convert data to JSON-safe format"""
                if isinstance(data, dict):
                    return {k: make_json_safe(v) for k, v in data.items()}
                elif isinstance(data, list):
                    return [make_json_safe(item) for item in data]
                elif isinstance(data, (pd.Timestamp, datetime)):
                    return str(data)
                elif isinstance(data, (np.integer, np.floating)):
                    return float(data)
                elif pd.isna(data):
                    return None
                else:
                    return str(data)
            
            if viz_type == 'bar':
                # Count frequency of categories
                col = viz_config.get('x')
                if not col or col not in self.df.columns:
                    return []
                
                data = self.df[col].value_counts().reset_index()
                data.columns = [col, 'count']
                return make_json_safe(data.head(20).to_dict('records'))
            
            elif viz_type == 'histogram':
                # Create bins for histogram
                col = viz_config.get('x')
                if not col or col not in self.df.columns:
                    return {'bins': [], 'counts': []}
                
                # Get numeric data only
                numeric_data = pd.to_numeric(self.df[col], errors='coerce').dropna()
                
                if len(numeric_data) == 0:
                    return {'bins': [], 'counts': []}
                
                data, bins = np.histogram(numeric_data, bins=20)
                return {
                    'bins': [float(b) for b in bins.tolist()],
                    'counts': [int(c) for c in data.tolist()]
                }
            
            elif viz_type == 'scatter':
                # Get x, y pairs
                x_col = viz_config.get('x')
                y_col = viz_config.get('y')
                
                if not x_col or not y_col or x_col not in self.df.columns or y_col not in self.df.columns:
                    return []
                
                data = self.df[[x_col, y_col]].copy()
                
                # Convert to numeric
                data[x_col] = pd.to_numeric(data[x_col], errors='coerce')
                data[y_col] = pd.to_numeric(data[y_col], errors='coerce')
                data = data.dropna()
                
                return make_json_safe(data.head(1000).to_dict('records'))
            
            elif viz_type == 'line':
                # Group by time and aggregate
                x_col = viz_config.get('x')
                y_col = viz_config.get('y')
                
                if not x_col or not y_col or x_col not in self.df.columns or y_col not in self.df.columns:
                    return []
                
                # Convert y to numeric
                df_copy = self.df.copy()
                df_copy[y_col] = pd.to_numeric(df_copy[y_col], errors='coerce')
                
                data = df_copy.groupby(x_col)[y_col].mean().reset_index()
                return make_json_safe(data.head(100).to_dict('records'))
            
            elif viz_type == 'pie':
                # Count frequency
                col = viz_config.get('category')
                if not col or col not in self.df.columns:
                    return []
                
                data = self.df[col].value_counts().reset_index()
                data.columns = ['category', 'value']
                return make_json_safe(data.head(10).to_dict('records'))
            
            elif viz_type == 'heatmap':
                # Correlation matrix
                columns = viz_config.get('columns', [])
                
                # Filter to only numeric columns that exist
                numeric_cols = []
                for col in columns:
                    if col in self.df.columns:
                        try:
                            pd.to_numeric(self.df[col], errors='raise')
                            numeric_cols.append(col)
                        except:
                            pass
                
                if len(numeric_cols) < 2:
                    return {'columns': [], 'correlation': []}
                
                corr_matrix = self.df[numeric_cols].corr()
                return {
                    'columns': numeric_cols,
                    'correlation': [[float(v) if not pd.isna(v) else 0 for v in row] for row in corr_matrix.values.tolist()]
                }
            
            return []
            
        except Exception as e:
            print(f"Error preparing visualization: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def export_cleaned_data(self, output_path):
        """Export cleaned data"""
        if output_path.endswith('.csv'):
            self.df.to_csv(output_path, index=False)
        elif output_path.endswith('.xlsx'):
            self.df.to_excel(output_path, index=False)
        
        return output_path
    
    def get_summary(self):
        """Get data summary"""
        # Convert data preview to handle datetime objects
        preview_data = []
        if self.df is not None and not self.df.empty:
            for _, row in self.df.head(10).iterrows():
                row_dict = {}
                for col, val in row.items():
                    # Convert datetime/timestamp to string
                    if pd.api.types.is_datetime64_any_dtype(type(val)) or isinstance(val, pd.Timestamp):
                        row_dict[col] = str(val)
                    elif pd.isna(val):
                        row_dict[col] = None
                    elif isinstance(val, (np.integer, np.floating)):
                        row_dict[col] = float(val)
                    else:
                        row_dict[col] = str(val)
                preview_data.append(row_dict)
        
        return {
            'total_rows': len(self.df) if self.df is not None else 0,
            'total_columns': len(self.df.columns) if self.df is not None else 0,
            'columns': self.metadata.get('columns', {}),
            'cleaning_report': self.cleaning_report,
            'data_preview': preview_data
        }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print(json.dumps({"success": False, "error": "Usage: python smart_processor.py <command> <filepath>"}))
        sys.exit(1)
    
    command = sys.argv[1]
    filepath = sys.argv[2]
    
    processor = SmartDataProcessor()
    
    try:
        if command == "analyze":
            # Load and analyze data
            if not processor.load_data(filepath):
                print(json.dumps({
                    "success": False,
                    "error": "Failed to load file",
                    "cleaning_report": processor.cleaning_report
                }))
                sys.exit(1)
            
            column_info = processor.analyze_columns()
            
            if not column_info:
                print(json.dumps({
                    "success": False,
                    "error": "No columns found in file",
                    "cleaning_report": processor.cleaning_report
                }))
                sys.exit(1)
            
            processor.clean_data()
            suggestions = processor.get_visualization_suggestions()
            
            result = {
                "success": True,
                "summary": processor.get_summary(),
                "visualization_suggestions": suggestions
            }
            
            print(json.dumps(result))
        
        elif command == "prepare_viz":
            # Prepare data for specific visualization
            # Read viz_config from stdin or file to avoid Windows command line escaping issues
            try:
                if len(sys.argv) > 3:
                    # Try to parse from argument first
                    viz_config_str = sys.argv[3]
                    # Handle both raw JSON and file path
                    if viz_config_str.startswith('{'):
                        viz_config = json.loads(viz_config_str)
                    else:
                        # It's a file path
                        with open(viz_config_str, 'r') as f:
                            viz_config = json.load(f)
                else:
                    # Read from stdin
                    viz_config = json.load(sys.stdin)
            except json.JSONDecodeError as e:
                print(json.dumps({
                    "success": False,
                    "error": f"Invalid JSON in viz_config: {str(e)}",
                    "type": "JSONDecodeError",
                    "raw_input": sys.argv[3] if len(sys.argv) > 3 else "stdin"
                }))
                sys.exit(1)
            
            if not processor.load_data(filepath):
                print(json.dumps({"success": False, "error": "Failed to load file"}))
                sys.exit(1)
            
            processor.analyze_columns()
            processor.clean_data()
            
            viz_data = processor.prepare_visualization_data(viz_config)
            
            result = {
                "success": True,
                "data": viz_data
            }
            
            print(json.dumps(result))
        
        else:
            print(json.dumps({"success": False, "error": f"Unknown command: {command}"}))
            sys.exit(1)
            
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "type": type(e).__name__
        }))
        sys.exit(1)