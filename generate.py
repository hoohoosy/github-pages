import pandas as pd
from datetime import datetime, timedelta

def generate_dashboard():
    # 1. 데이터 로드
    df = pd.read_csv('STAT_daily_reve.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # SumReve0, 1, 2를 합친 총합 계산 (필요시 수정 가능)
    df['Total'] = df['SumReve0'] + df['SumReve1'] + df['SumReve2']

    # 2. 주요 지표 계산
    latest_total = df['Total'].iloc[-1]
    
    def get_diff(days):
        target_date = df['Date'].iloc[-1] - timedelta(days=days)
        past_data = df[df['Date'] <= target_date]
        if not past_data.empty:
            return latest_total - past_data['Total'].iloc[-1]
        return 0.0

    diff_1d = latest_total - (df['Total'].iloc[-2] if len(df) > 1 else latest_total)
    diff_1w = get_diff(7)
    diff_1m = get_diff(30)

    # 3. HTML 템플릿 읽기 및 데이터 주입
    with open('template.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 데이터 치환
    html = html.replace('{{LATEST_TOTAL}}', f"{latest_total:,.1f}")
    html = html.replace('{{DIFF_1D}}', f"{diff_1d:+,.1f}")
    html = html.replace('{{DIFF_1W}}', f"{diff_1w:+,.1f}")
    html = html.replace('{{DIFF_1M}}', f"{diff_1m:+,.1f}")
    html = html.replace('{{LABELS}}', str(df['Date'].dt.strftime('%m-%d').tolist()))
    html = html.replace('{{DATA}}', str(df['Total'].tolist()))
    html = html.replace('{{UPDATE_TIME}}', datetime.now().strftime('%Y-%m-%d %H:%M'))

    with open('dashboard_raw.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    generate_dashboard()