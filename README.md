# Exam Result System — Separate Helm Charts (per service)

Har component ka apna independent Helm chart hai, taake ArgoCD mein har ek ko
alag `Application` ke through separately manage/sync kiya ja sake.

```
charts/
├── namespace/         # exam-board namespace
├── postgres/           # Secret + PV + PVC + Service + StatefulSet
├── admin-service/      # Deployment + Service (Django admin app, port 8001)
├── student-service/    # Deployment + Service (Django student app, port 8000)
├── ingress/             # nginx Ingress (/admin, /student paths)
└── argocd-apps/         # ArgoCD Application manifests, 1 per chart
```

## Manual install order (bina ArgoCD ke, plain helm)

```bash
helm install namespace ./namespace
helm install postgres ./postgres
helm install admin-service ./admin-service
helm install student-service ./student-service
helm install ingress ./ingress
```

Sab charts `namespace: exam-board` ko `values.yaml` se lete hain — chart khud
namespace create nahi karta (sirf `namespace` chart karta hai), so pehle wo
apply karo.

## ArgoCD se deploy karna

1. `argocd-apps/*.yaml` files mein `repoURL` ko apne actual git repo se replace karo
   (jahan ye `charts/` folder push hoga).
2. Phir apply karo:

```bash
kubectl apply -f charts/argocd-apps/namespace-app.yaml
kubectl apply -f charts/argocd-apps/postgres-app.yaml
kubectl apply -f charts/argocd-apps/admin-service-app.yaml
kubectl apply -f charts/argocd-apps/student-service-app.yaml
kubectl apply -f charts/argocd-apps/ingress-app.yaml
```

Har `Application` ka apna `sync-wave` set hai (namespace → postgres →
services → ingress), aur andar ke Kubernetes objects par bhi wahi sync-wave
annotations maujood hain jo original manifests mein thin — dono level pe
ordering control hoti hai.

Alternative: agar chaho to ek **App-of-Apps** pattern bhi bana sakte ho (ek
parent Application jo in 5 Applications ko generate kare) — bata do to wo bhi
bana deta hoon.

## Values override (example — CI/CD mein image tag update)

```bash
helm upgrade admin-service ./admin-service --set image.tag=v1.3.0 -n exam-board
helm upgrade student-service ./student-service --set image.tag=v1.3.0 -n exam-board
```

Ya ArgoCD Application ke andar `spec.source.helm.values` block use karo
(commented example har `argocd-apps/*.yaml` mein diya hua hai).

## Defaults / secrets

`postgres/values.yaml`, `admin-service/values.yaml`,
`student-service/values.yaml` mein wahi placeholder defaults hain jo original
k8s manifests mein thay (`postgres`/`postgres`, `change-this-secret-key`,
`Admin@12345`). Production mein zaroor override karo.
# argocd-exam-board-kind
