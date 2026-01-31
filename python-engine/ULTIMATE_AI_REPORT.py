#!/usr/bin/env python3
"""
FINAL COMPLETE REPORT - Everything included!
"""
import pandas as pd
import numpy as np
import json
import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from scipy import stats
from sklearn.linear_model import LinearRegression

class FinalCompleteReport:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.numeric_cols = []
        self.categorical_cols = []
        self.datetime_cols = []
        
        self.current_state = {}
        self.patterns = {}
        self.predictions = {}
        self.recommendations = []
        
    def load_and_analyze(self):
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            else:
                self.df = pd.read_excel(self.filepath)
            
            print(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns", file=sys.stderr)
            
            for col in self.df.columns:
                try:
                    self.df[col] = pd.to_numeric(self.df[col], errors='raise')
                    self.numeric_cols.append(col)
                except:
                    try:
                        pd.to_datetime(self.df[col], errors='raise')
                        self.datetime_cols.append(col)
                    except:
                        if self.df[col].nunique() < 50:
                            self.categorical_cols.append(col)
            
            print(f"Found {len(self.numeric_cols)} numeric columns", file=sys.stderr)
            
            self.analyze_current_state()
            self.analyze_patterns()
            self.make_predictions()
            self.generate_detailed_recommendations()  # RESTORED!
            
            print(f"Generated {len(self.recommendations)} recommendations", file=sys.stderr)
            
            return True
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return False
    
    def analyze_current_state(self):
        self.current_state['overview'] = {
            'total_records': len(self.df),
            'total_variables': len(self.df.columns),
            'data_quality': f"{(1 - self.df.isnull().sum().sum()/(len(self.df)*len(self.df.columns)))*100:.1f}%",
            'analysis_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        self.current_state['metrics'] = []
        for col in self.numeric_cols[:5]:
            self.current_state['metrics'].append({
                'name': col,
                'current_value': float(self.df[col].iloc[-1]) if len(self.df) > 0 else 0,
                'average': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'std': float(self.df[col].std()),
                'trend': 'increasing' if self.df[col].iloc[-1] > self.df[col].mean() else 'decreasing'
            })
    
    def analyze_patterns(self):
        self.patterns['trends'] = []
        
        for col in self.numeric_cols[:5]:
            if len(self.df) >= 3:
                values = self.df[col].dropna()
                if len(values) >= 3:
                    x = np.arange(len(values))
                    y = values.values
                    
                    try:
                        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                        
                        self.patterns['trends'].append({
                            'metric': col,
                            'direction': 'Upward' if slope > 0 else 'Downward',
                            'strength': 'Strong' if abs(r_value) > 0.7 else 'Moderate' if abs(r_value) > 0.4 else 'Weak',
                            'r_squared': f"{r_value**2:.3f}",
                            'r_value': r_value,
                            'slope': slope,
                            'growth_rate': f"{slope:.2f} per period",
                            'explanation': f"{col} is {'strongly' if abs(r_value) > 0.7 else 'moderately' if abs(r_value) > 0.4 else 'slightly'} {'increasing' if slope > 0 else 'decreasing'} over time with R² = {r_value**2:.3f}. This trend is {'reliable' if abs(r_value) > 0.7 else 'moderate' if abs(r_value) > 0.4 else 'weak'}..."
                        })
                    except Exception as e:
                        print(f"Trend error for {col}: {e}", file=sys.stderr)
        
        self.patterns['correlations'] = []
        if len(self.numeric_cols) >= 2:
            try:
                corr_matrix = self.df[self.numeric_cols[:6]].corr()
                
                for i in range(len(self.numeric_cols[:6])):
                    for j in range(i+1, len(self.numeric_cols[:6])):
                        corr_val = corr_matrix.iloc[i, j]
                        
                        if abs(corr_val) > 0.5:
                            self.patterns['correlations'].append({
                                'variable1': self.numeric_cols[i],
                                'variable2': self.numeric_cols[j],
                                'correlation': f"{corr_val:.3f}",
                                'corr_value': corr_val,
                                'type': 'Positive' if corr_val > 0 else 'Negative',
                                'strength': 'Strong' if abs(corr_val) > 0.7 else 'Moderate',
                                'explanation': f"When {self.numeric_cols[i]} goes up, {self.numeric_cols[j]} typically {'increases' if corr_val > 0 else 'decreases'}. This {'strong' if abs(corr_val) > 0.7 else 'moderate'} {'positive' if corr_val > 0 else 'negative'} relationship (r={corr_val:.3f}) can be used for predictive modeling."
                            })
            except Exception as e:
                print(f"Correlation error: {e}", file=sys.stderr)
    
    def make_predictions(self):
        print("Starting predictions...", file=sys.stderr)
        
        self.predictions['forecasts'] = []
        self.predictions['risks'] = []
        self.predictions['opportunities'] = []
        
        for col in self.numeric_cols[:5]:
            print(f"Predicting {col}...", file=sys.stderr)
            
            try:
                values = self.df[col].dropna()
                
                if len(values) < 3:
                    continue
                
                X = np.arange(len(values)).reshape(-1, 1)
                y = values.values
                
                model = LinearRegression()
                model.fit(X, y)
                
                current = float(values.iloc[-1])
                pred_1 = float(model.predict([[len(values)]])[0])
                pred_3 = float(model.predict([[len(values) + 2]])[0])
                pred_5 = float(model.predict([[len(values) + 4]])[0])
                pred_10 = float(model.predict([[len(values) + 9]])[0])
                
                change = pred_5 - current
                change_pct = (change / current * 100) if current != 0 else 0
                
                r_squared = model.score(X, y)
                
                predictions_all = model.predict(X)
                residuals = y - predictions_all
                std_error = float(np.std(residuals))
                confidence_95 = 1.96 * std_error
                
                forecast = {
                    'metric': col,
                    'current_value': f"{current:.2f}",
                    'predicted_1': f"{pred_1:.2f}",
                    'predicted_3': f"{pred_3:.2f}",
                    'predicted_5': f"{pred_5:.2f}",
                    'predicted_10': f"{pred_10:.2f}",
                    'change_5period': f"{change:.2f}",
                    'change_percent': f"{change_pct:.1f}%",
                    'change_pct_value': change_pct,
                    'r_squared_value': r_squared,
                    'direction': '↗ Increase' if change > 0 else '↘ Decrease',
                    'confidence': 'High' if r_squared > 0.7 else 'Medium' if r_squared > 0.4 else 'Low',
                    'confidence_score': f"{r_squared:.3f}",
                    'confidence_interval': f"±{confidence_95:.2f}",
                    'explanation': f"Based on historical patterns (R²={r_squared:.3f}), {col} is forecasted to {'increase' if change > 0 else 'decrease'} by {abs(change_pct):.1f}% over the next 5 periods. The prediction has {('high' if r_squared > 0.7 else 'medium' if r_squared > 0.4 else 'low')} reliability with a confidence interval of ±{confidence_95:.2f}."
                }
                
                self.predictions['forecasts'].append(forecast)
                print(f"✓ Predicted {col}: {change_pct:.1f}%", file=sys.stderr)
                
                if change_pct < -5 and r_squared > 0.3:
                    self.predictions['risks'].append({
                        'metric': col,
                        'risk_level': 'Critical' if change_pct < -20 else 'High' if change_pct < -10 else 'Medium',
                        'predicted_decline': f"{change_pct:.1f}%",
                        'confidence': 'High' if r_squared > 0.7 else 'Medium',
                        'mitigation': self._generate_mitigation(col, change_pct)
                    })
                
                if change_pct > 5 and r_squared > 0.3:
                    self.predictions['opportunities'].append({
                        'metric': col,
                        'growth_potential': f"{change_pct:.1f}%",
                        'predicted_value': f"{pred_5:.2f}",
                        'confidence': 'High' if r_squared > 0.7 else 'Medium',
                        'action': self._generate_opportunity_action(col, change_pct),
                        'expected_roi': f"{change_pct * 1.5:.1f}% potential ROI"
                    })
                    
            except Exception as e:
                print(f"ERROR predicting {col}: {str(e)}", file=sys.stderr)
        
        print(f"Total forecasts: {len(self.predictions['forecasts'])}", file=sys.stderr)
    
    def _generate_mitigation(self, metric, decline_pct):
        """Generate specific mitigation strategies"""
        strategies = {
            'Bounce Rate': "1. Improve landing page UX/UI design\n2. Reduce page load time to <2 seconds\n3. Implement A/B testing on high-bounce pages\n4. Add compelling CTAs above the fold\n5. Review and optimize mobile responsiveness",
            'Time on Site': "1. Create more engaging content (videos, interactive elements)\n2. Implement internal linking strategy\n3. Add related content recommendations\n4. Improve content readability (headers, bullets)\n5. Create content series to encourage return visits",
            'Visitors': "1. Launch targeted digital marketing campaigns\n2. Optimize SEO for high-intent keywords\n3. Invest in paid acquisition channels (Google Ads, Social)\n4. Implement referral program\n5. Improve organic social media presence",
            'Conversions': "1. Streamline checkout/conversion funnel\n2. Add trust signals (reviews, badges, guarantees)\n3. Implement exit-intent popups\n4. A/B test pricing and messaging\n5. Offer time-limited incentives",
            'Response Time': "1. Optimize resource allocation\n2. Implement predictive dispatch\n3. Add staff during peak periods\n4. Review and streamline protocols\n5. Invest in training and equipment"
        }
        
        for key in strategies:
            if key.lower() in metric.lower():
                return strategies[key]
        
        return "1. Conduct root cause analysis\n2. Benchmark against industry standards\n3. Implement monitoring dashboards\n4. Test corrective interventions\n5. Review and adjust strategy monthly"
    
    def _generate_opportunity_action(self, metric, growth_pct):
        """Generate opportunity actions"""
        actions = {
            'Page Views': "1. Scale successful content types (identified through analytics)\n2. Increase publishing frequency by 2x\n3. Expand into new content categories\n4. Launch content distribution partnerships\n5. Invest in content promotion (paid + organic)",
            'Visitors': f"1. Double down on highest-performing channels\n2. Launch lookalike audience campaigns\n3. Expand geographic targeting\n4. Increase marketing budget by {growth_pct/2:.0f}%\n5. Develop strategic partnerships for co-marketing",
            'Time on Site': "1. Create longer-form, in-depth content\n2. Build interactive tools and calculators\n3. Launch video content series\n4. Implement personalization engine\n5. Create membership/community features",
            'Conversions': "1. Optimize conversion funnel (reduce steps by 30%)\n2. Launch upsell/cross-sell campaigns\n3. Implement cart abandonment recovery\n4. Test premium pricing tiers\n5. Scale winning variations from A/B tests",
            'Revenue': f"1. Scale successful revenue streams\n2. Expand into adjacent markets\n3. Launch premium offerings\n4. Increase prices strategically (+{growth_pct/3:.0f}%)\n5. Develop new revenue channels"
        }
        
        for key in actions:
            if key.lower() in metric.lower():
                return actions[key]
        
        return "1. Allocate additional resources to capitalize on growth\n2. Scale successful initiatives\n3. Expand market reach\n4. Invest in automation and optimization\n5. Monitor and maintain momentum"
    
    def generate_detailed_recommendations(self):
        """DETAILED ACTIONABLE RECOMMENDATIONS - RESTORED!"""
        print("Generating recommendations...", file=sys.stderr)
        
        # From upward trends
        for trend in self.patterns.get('trends', []):
            if trend['strength'] in ['Strong', 'Moderate'] and trend['direction'] == 'Upward':
                self.recommendations.append({
                    'priority': 'High',
                    'category': 'Growth Opportunity',
                    'recommendation': f"Capitalize on {trend['metric']} growth momentum",
                    'current_state': f"Growing at {trend['growth_rate']} with {trend['strength'].lower()} trend (R²={trend['r_squared']})",
                    'action_plan': self._generate_opportunity_action(trend['metric'], 15),
                    'expected_outcome': f"Sustained growth at current rate ({trend['growth_rate']})",
                    'timeline': '30-90 days',
                    'kpis': f"Target: Maintain R² >{trend['r_squared']}, Increase growth rate by 20%"
                })
        
        # From downward trends
        for trend in self.patterns.get('trends', []):
            if trend['strength'] in ['Strong', 'Moderate'] and trend['direction'] == 'Downward':
                self.recommendations.append({
                    'priority': 'High',
                    'category': 'Risk Mitigation',
                    'recommendation': f"Address declining {trend['metric']}",
                    'current_state': f"Declining at {trend['growth_rate']} with {trend['strength'].lower()} trend (R²={trend['r_squared']})",
                    'action_plan': self._generate_mitigation(trend['metric'], -15),
                    'expected_outcome': f"Stabilize metric and reverse decline to positive growth",
                    'timeline': '60-90 days',
                    'kpis': f"Target: Reduce decline rate by 50% in 30 days, achieve positive growth in 90 days"
                })
        
        # From correlations
        for corr in self.patterns.get('correlations', [])[:3]:
            self.recommendations.append({
                'priority': 'Medium',
                'category': 'Strategic Insight',
                'recommendation': f"Leverage {corr['variable1']}-{corr['variable2']} relationship",
                'current_state': f"{corr['strength']} {corr['type'].lower()} correlation (r={corr['correlation']})",
                'action_plan': f"1. Use {corr['variable1']} as leading indicator for {corr['variable2']}\n2. Set up automated alerts when {corr['variable1']} changes >10%\n3. Build predictive model using this relationship\n4. Create dashboard showing both metrics together\n5. Optimize {corr['variable1']} to improve {corr['variable2']}",
                'expected_outcome': f"Improved forecasting accuracy and proactive decision-making",
                'timeline': '14-30 days',
                'kpis': f"Forecasting accuracy >85%, Response time to changes <24 hours"
            })
        
        # From risks
        for risk in self.predictions.get('risks', []):
            self.recommendations.append({
                'priority': 'Critical' if risk['risk_level'] == 'Critical' else 'High',
                'category': 'Urgent Action Required',
                'recommendation': f"Prevent predicted {risk['metric']} decline",
                'current_state': f"Forecasted decline of {risk['predicted_decline']} with {risk['confidence']} confidence",
                'action_plan': risk['mitigation'],
                'expected_outcome': f"Prevent decline, stabilize at current levels or better",
                'timeline': 'Immediate (7-14 days)',
                'kpis': f"Stop decline within 14 days, achieve 0% change or positive growth within 30 days"
            })
        
        # From opportunities
        for opp in self.predictions.get('opportunities', [])[:3]:
            self.recommendations.append({
                'priority': 'High',
                'category': 'Growth Acceleration',
                'recommendation': f"Accelerate {opp['metric']} growth trajectory",
                'current_state': f"Strong growth predicted: {opp['growth_potential']} with {opp['confidence']} confidence",
                'action_plan': opp['action'],
                'expected_outcome': f"Achieve predicted growth of {opp['growth_potential']}, {opp['expected_roi']}",
                'timeline': '30-60 days',
                'kpis': f"Hit target: {opp['predicted_value']}, ROI > {opp['expected_roi'].split('%')[0]}%"
            })
        
        print(f"Generated {len(self.recommendations)} recommendations", file=sys.stderr)
    
    def generate_pdf(self, output_filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(script_dir, '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        output_path = os.path.join(reports_dir, output_filename)
        
        doc = SimpleDocTemplate(output_path, pagesize=landscape(letter),
                               topMargin=0.5*inch, bottomMargin=0.5*inch,
                               leftMargin=0.5*inch, rightMargin=0.5*inch)
        
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=28,
                                    textColor=colors.HexColor('#1e3a8a'), alignment=TA_CENTER,
                                    fontName='Helvetica-Bold', spaceAfter=12)
        
        section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=18,
                                      textColor=colors.HexColor('#1e3a8a'), fontName='Helvetica-Bold',
                                      spaceAfter=10, spaceBefore=15)
        
        # COVER
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph("ANALYTICS REPORT", title_style))
        #story.append(Paragraph("Predictive Intelligence & Strategic Insights", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        story.append(PageBreak())
        
        # SECTION 1
        story.append(Paragraph("📊 SECTION 1: WHAT IS HAPPENING", section_style))
        overview = self.current_state['overview']
        overview_data = [['Metric', 'Value'],
                        ['Total Records', f"{overview['total_records']:,}"],
                        ['Total Variables', str(overview['total_variables'])],
                        ['Data Quality', overview['data_quality']],
                        ['Analysis Date', overview['analysis_date']]]
        overview_table = Table(overview_data, colWidths=[3*inch, 2*inch])
        overview_table.setStyle(self._get_blue_table_style())
        story.append(overview_table)
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("<b>Key Performance Metrics:</b>", styles['Normal']))
        metrics_data = [['Metric', 'Current', 'Average', 'Min', 'Max', 'Trend']]
        for m in self.current_state['metrics']:
            metrics_data.append([m['name'], f"{m['current_value']:.2f}", f"{m['average']:.2f}",
                                f"{m['min']:.2f}", f"{m['max']:.2f}", m['trend'].title()])
        metrics_table = Table(metrics_data)
        metrics_table.setStyle(self._get_blue_table_style())
        story.append(metrics_table)
        story.append(PageBreak())
        
        # SECTION 2
        story.append(Paragraph("🔍 SECTION 2: HOW IT'S HAPPENING", section_style))
        if self.patterns.get('trends'):
            story.append(Paragraph("<b>Trend Analysis:</b>", styles['Normal']))
            trend_data = [['Metric', 'Direction', 'Strength', 'R²', 'Growth Rate', 'Explanation']]
            for t in self.patterns['trends']:
                trend_data.append([t['metric'], t['direction'], t['strength'], t['r_squared'],
                                  t['growth_rate'], t['explanation'][:80] + '...'])
            trend_table = Table(trend_data, colWidths=[1.2*inch, 1*inch, 1*inch, 0.8*inch, 1.2*inch, 3*inch])
            trend_table.setStyle(self._get_green_table_style())
            story.append(trend_table)
            story.append(Spacer(1, 0.2*inch))
        
        if self.patterns.get('correlations'):
            story.append(Paragraph("<b>Key Relationships:</b>", styles['Normal']))
            corr_data = [['Variable 1', 'Variable 2', 'Correlation', 'Type', 'Explanation']]
            for c in self.patterns['correlations']:
                corr_data.append([c['variable1'], c['variable2'], c['correlation'], c['type'],
                                 c['explanation'][:100] + '...'])
            corr_table = Table(corr_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch, 4*inch])
            corr_table.setStyle(self._get_green_table_style())
            story.append(corr_table)
        
        story.append(PageBreak())
        
        # SECTION 3 - PREDICTIONS
        story.append(Paragraph("🔮 SECTION 3: WHAT WILL HAPPEN", section_style))
        story.append(Paragraph("Predictive Forecasting & Future Outlook", styles['Heading3']))
        story.append(Spacer(1, 0.2*inch))
        
        if self.predictions.get('forecasts'):
            story.append(Paragraph("<b>Multi-Period Forecasts:</b>", styles['Normal']))
            story.append(Paragraph("Predictions for next 1, 3, 5, and 10 periods with confidence intervals", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            forecast_data = [['Metric', 'Current', '+1', '+3', '+5', '+10', 'Change', 'Confidence', 'CI']]
            for f in self.predictions['forecasts']:
                forecast_data.append([f['metric'], f['current_value'], f['predicted_1'], f['predicted_3'],
                                     f['predicted_5'], f['predicted_10'], f['change_percent'],
                                     f['confidence'], f['confidence_interval']])
            
            forecast_table = Table(forecast_data, colWidths=[1.3*inch, 0.9*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.9*inch, 0.9*inch, 0.8*inch])
            forecast_table.setStyle(self._get_purple_table_style())
            story.append(forecast_table)
            story.append(Spacer(1, 0.3*inch))
            
            story.append(Paragraph("<b>Forecast Explanations:</b>", styles['Normal']))
            for f in self.predictions['forecasts']:
                story.append(Paragraph(f"<b>{f['metric']}:</b> {f['explanation']}", styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
        
        story.append(PageBreak())
        
        # Risks & Opportunities
        if self.predictions.get('risks'):
            story.append(Paragraph("<b>⚠️ Risk Assessment:</b>", styles['Normal']))
            risk_data = [['Metric', 'Risk Level', 'Predicted Decline', 'Mitigation Strategy']]
            for r in self.predictions['risks']:
                risk_data.append([r['metric'], r['risk_level'], r['predicted_decline'], r['mitigation'][:150] + '...'])
            risk_table = Table(risk_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 4*inch])
            risk_table.setStyle(self._get_red_table_style())
            story.append(risk_table)
            story.append(Spacer(1, 0.2*inch))
        
        if self.predictions.get('opportunities'):
            story.append(Paragraph("<b>✨ Growth Opportunities:</b>", styles['Normal']))
            opp_data = [['Metric', 'Growth Potential', 'Predicted Value', 'Action Plan']]
            for o in self.predictions['opportunities']:
                opp_data.append([o['metric'], o['growth_potential'], o['predicted_value'], o['action'][:120] + '...'])
            opp_table = Table(opp_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 4.5*inch])
            opp_table.setStyle(self._get_green_highlight_table_style())
            story.append(opp_table)
        
        story.append(PageBreak())
        
        # SECTION 4 - RECOMMENDATIONS (COMPLETE!)
        story.append(Paragraph("✅ STRATEGIC RECOMMENDATIONS", section_style))
        story.append(Paragraph("Prioritized, Actionable Recommendations with Timelines & KPIs", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        if self.recommendations:
            rec_data = [['Priority', 'Category', 'Recommendation', 'Action Plan (Top 3)', 'Timeline', 'KPIs']]
            for r in self.recommendations:
                actions = r['action_plan'].split('\n')[:3]
                action_summary = '\n'.join(actions)
                
                rec_data.append([
                    r['priority'],
                    r['category'],
                    r['recommendation'],
                    action_summary,
                    r.get('timeline', 'N/A'),
                    r.get('kpis', 'Monitor progress')[:60] + '...'
                ])
            
            rec_table = Table(rec_data, colWidths=[0.8*inch, 1.2*inch, 1.8*inch, 2.5*inch, 1*inch, 1.5*inch])
            rec_table.setStyle(self._get_blue_table_style())
            story.append(rec_table)
        else:
            story.append(Paragraph("No specific recommendations generated. More data needed for detailed insights.", styles['Normal']))
        
        doc.build(story)
        return output_path
    
    def _get_blue_table_style(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightblue]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
    
    def _get_green_table_style(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
    
    def _get_purple_table_style(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#faf5ff')]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
    
    def _get_red_table_style(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
    
    def _get_green_highlight_table_style(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d1fae5')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No filepath"}))
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    report = FinalCompleteReport(filepath)
    
    if not report.load_and_analyze():
        print(json.dumps({"success": False, "error": "Failed to analyze"}))
        sys.exit(1)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"Report_{timestamp}.pdf"
    
    output_path = report.generate_pdf(output_filename)
    
    print(json.dumps({
        "success": True,
        "filename": output_filename,
        "path": output_path,
        "predictions_count": len(report.predictions.get('forecasts', [])),
        "recommendations_count": len(report.recommendations)
    }))