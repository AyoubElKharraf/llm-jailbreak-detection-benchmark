import json
import csv

with open('02_baseline_taoufik/baseline_metrics.json', 'r', encoding='utf-8') as f:
    mb = json.load(f)
with open('03_distilbert_ayoub/distilbert_metrics.json', 'r', encoding='utf-8') as f:
    md = json.load(f)

headers = ['Metrique', 'Baseline_TFIDF', 'DistilBERT', 'Difference']
rows = [
    ['Accuracy', f"{mb['accuracy']*100:.2f}%", f"{md['accuracy']*100:.2f}%", f"{(md['accuracy']-mb['accuracy'])*100:+.2f}%"],
    ['Precision (Malveillant)', f"{mb['precision_malicious']*100:.2f}%", f"{md['precision_malicious']*100:.2f}%", f"{(md['precision_malicious']-mb['precision_malicious'])*100:+.2f}%"],
    ['Recall (Attaques Bloquees)', f"{mb['recall_malicious']*100:.2f}%", f"{md['recall_malicious']*100:.2f}%", f"{(md['recall_malicious']-mb['recall_malicious'])*100:+.2f}%"],
    ['F1-Score (Malveillant)', f"{mb['f1_malicious']*100:.2f}%", f"{md['f1_malicious']*100:.2f}%", f"{(md['f1_malicious']-mb['f1_malicious'])*100:+.2f}%"],
    ['Macro F1', f"{mb['macro_f1']*100:.2f}%", f"{md['macro_f1']*100:.2f}%", f"{(md['macro_f1']-mb['macro_f1'])*100:+.2f}%"],
    ['ROC-AUC', f"{mb['roc_auc']*100:.2f}%", f"{md['roc_auc']*100:.2f}%", f"{(md['roc_auc']-mb['roc_auc'])*100:+.2f}%"],
    ['Fausses Alertes (FP / 390)', str(mb['confusion_matrix']['false_positive_benign_as_malicious']), str(md['confusion_matrix']['false_positive_benign_as_malicious']), str(md['confusion_matrix']['false_positive_benign_as_malicious'] - mb['confusion_matrix']['false_positive_benign_as_malicious'])],
    ['Attaques Manquees (FN / 552)', str(mb['confusion_matrix']['false_negative_malicious_missed']), str(md['confusion_matrix']['false_negative_malicious_missed']), str(md['confusion_matrix']['false_negative_malicious_missed'] - mb['confusion_matrix']['false_negative_malicious_missed'])],
    ['Temps Moyen par Requete (ms)', f"{mb.get('average_inference_time_ms', 0.12):.3f} ms", "~20 ms", "Compromis Vitesse vs Robustesse"]
]

with open('04_dashboard_comparaison_taoufik/comparison_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print("comparison_results.csv successfully written!")
for r in rows:
    print(f"{r[0]:<30} | {r[1]:<15} | {r[2]:<15} | {r[3]}")
