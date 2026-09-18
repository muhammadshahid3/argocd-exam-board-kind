{{- define "postgres.syncWave" -}}
{{- if .root.Values.argocd.enabled }}
argocd.argoproj.io/sync-wave: {{ .wave | quote }}
{{- end }}
{{- end }}
