def compute_risk_score(total_anomalies, total_rows):

    if total_rows == 0:
        return 0

    ratio = total_anomalies / total_rows

    score = ratio * 100

    return round(score, 2)