#!/usr/bin/env python3
"""
Enhanced chart data with ALL types including Gantt
"""
import pandas as pd
import numpy as np
import json
import sys
from datetime import timedelta

if len(sys.argv) < 4:
    print(json.dumps({"success": False, "error": "Missing arguments"}))
    sys.exit(1)

filepath = sys.argv[1]
command = sys.argv[2]
config_file = sys.argv[3]

# Load data
try:
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
except Exception as e:
    print(json.dumps({"success": False, "error": str(e)}))
    sys.exit(1)

# Load viz config
try:
    with open(config_file, 'r') as f:
        viz_config = json.load(f)
except Exception as e:
    print(json.dumps({"success": False, "error": f"Config error: {str(e)}"}))
    sys.exit(1)

# Prepare data
try:
    viz_type = viz_config.get('type')
    data_prep = viz_config.get('data_prep', 'basic')
    
    # Apply data range if specified (user selection)
    if 'data_range' in viz_config:
        start, end = viz_config['data_range']
        df = df.iloc[start:end+1]
    
    if data_prep == 'value_counts' or viz_type in ['pie', 'donut', 'bar', 'horizontal_bar']:
        col = viz_config.get('category') or viz_config.get('x')
        if col and col in df.columns:
            value_counts = df[col].value_counts().head(15)
            if viz_type in ['pie', 'donut']:
                data = [
                    {'category': str(idx), 'value': int(val)}
                    for idx, val in value_counts.items()
                ]
            else:
                data = [
                    {col: str(idx), 'count': int(val)}
                    for idx, val in value_counts.items()
                ]
        else:
            data = []
    
    elif data_prep == 'time_series' or viz_type in ['line', 'area']:
        x_col = viz_config.get('x')
        y_col = viz_config.get('y')
        
        if x_col in df.columns and y_col in df.columns:
            df_clean = df[[x_col, y_col]].dropna()
            df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
            df_clean = df_clean.dropna()
            
            try:
                df_clean[x_col] = pd.to_datetime(df_clean[x_col])
                df_clean = df_clean.sort_values(x_col)
                df_grouped = df_clean.groupby(x_col)[y_col].mean().reset_index()
                data = [
                    {x_col: str(row[x_col]), y_col: float(row[y_col])}
                    for _, row in df_grouped.head(100).iterrows()
                ]
            except:
                data = [
                    {x_col: str(row[x_col]), y_col: float(row[y_col])}
                    for _, row in df_clean.head(100).iterrows()
                ]
        else:
            data = []
    
    elif data_prep == 'correlation' or viz_type == 'scatter':
        x_col = viz_config.get('x')
        y_col = viz_config.get('y')
        
        if x_col in df.columns and y_col in df.columns:
            df_clean = df[[x_col, y_col]].dropna()
            df_clean[x_col] = pd.to_numeric(df_clean[x_col], errors='coerce')
            df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce')
            df_clean = df_clean.dropna()
            
            data = [
                {x_col: float(row[x_col]), y_col: float(row[y_col])}
                for _, row in df_clean.head(500).iterrows()
            ]
        else:
            data = []
    
    elif data_prep == 'gantt' or data_prep == 'gantt_synthetic' or viz_type == 'gantt':
        # GANTT CHART PREPARATION
        start_col = viz_config.get('start')
        end_col = viz_config.get('end')
        task_col = viz_config.get('task')
        
        if start_col and task_col and start_col in df.columns and task_col in df.columns:
            df_gantt = df[[start_col, task_col]].copy()
            
            if end_col and end_col in df.columns:
                df_gantt['end'] = df[end_col]
            else:
                # Synthetic end date (add 7 days)
                df_gantt[start_col] = pd.to_datetime(df_gantt[start_col], errors='coerce')
                df_gantt['end'] = df_gantt[start_col] + timedelta(days=7)
            
            df_gantt = df_gantt.dropna()
            df_gantt[start_col] = pd.to_datetime(df_gantt[start_col], errors='coerce')
            
            if 'end' in df_gantt.columns:
                df_gantt['end'] = pd.to_datetime(df_gantt['end'], errors='coerce')
            
            df_gantt = df_gantt.dropna()
            
            data = [
                {
                    'task': str(row[task_col]),
                    'start': str(row[start_col]),
                    'end': str(row['end']) if 'end' in row else str(row[start_col]),
                    'duration': (row['end'] - row[start_col]).days if 'end' in row else 7
                }
                for _, row in df_gantt.head(20).iterrows()
            ]
        else:
            data = []
    
    elif viz_type == 'bubble':
        x_col = viz_config.get('x')
        y_col = viz_config.get('y')
        size_col = viz_config.get('size')
        color_col = viz_config.get('color')
        
        cols_needed = [x_col, y_col, size_col, color_col]
        if all(c in df.columns for c in cols_needed if c):
            df_clean = df[cols_needed].dropna()
            
            for col in [x_col, y_col, size_col]:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
            df_clean = df_clean.dropna()
            
            data = [
                {
                    x_col: float(row[x_col]),
                    y_col: float(row[y_col]),
                    'size': float(row[size_col]),
                    'category': str(row[color_col])
                }
                for _, row in df_clean.head(100).iterrows()
            ]
        else:
            data = []
    
    elif viz_type == 'heatmap':
        columns = viz_config.get('columns', [])
        valid_cols = [c for c in columns if c in df.columns]
        
        if len(valid_cols) >= 2:
            df_numeric = df[valid_cols].apply(pd.to_numeric, errors='coerce').dropna()
            corr_matrix = df_numeric.corr()
            
            data = [
                {
                    'x': col1,
                    'y': col2,
                    'value': float(corr_matrix.loc[col1, col2])
                }
                for col1 in corr_matrix.columns
                for col2 in corr_matrix.index
            ]
        else:
            data = []
    
    elif viz_type == 'radar':
        category_col = viz_config.get('category')
        metrics = viz_config.get('metrics', [])
        
        valid_metrics = [m for m in metrics if m in df.columns]
        
        if category_col in df.columns and len(valid_metrics) >= 3:
            categories = df[category_col].unique()[:5]
            
            data = []
            for cat in categories:
                cat_data = df[df[category_col] == cat][valid_metrics].mean()
                for metric in valid_metrics:
                    data.append({
                        'subject': metric,
                        'value': float(cat_data.get(metric, 0)),
                        'category': str(cat)
                    })
        else:
            data = []
    
    else:
        data = []
    
    print(json.dumps({'success': True, 'data': data}))

except Exception as e:
    import traceback
    print(json.dumps({
        'success': False, 
        'error': str(e),
        'trace': traceback.format_exc()
    }))
    sys.exit(1)