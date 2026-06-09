# Автоматизированный контроль защиты данных

## 1. Контрольные точки

| Контрольная точка | Что проверяется | Инструменты | Условие прохождения |
|-------------------|-----------------|-------------|---------------------|
| **Git pre-commit / CI** | Нет секретов, private keys, паролей | Gitleaks, TruffleHog | Pipeline падает при найденном секрете |
| **SAST privacy rules** | Нет логирования PII/medical data | Semgrep | Pipeline падает при попытке логировать поля `pii`, `pii.sensitive`, `fin`, `hr` |
| **OpenAPI contract check** | API не возвращает чувствительные поля без политики | Spectral + OPA Conftest | Для каждого поля с тегом `pii.sensitive` есть ABAC policy |
| **Kubernetes policy check** | Нет plaintext secrets/env, включено шифрование secrets | OPA Gatekeeper / Kyverno | Нельзя применить манифест без шифрования и labels |
| **TLS monitoring** | Сертификаты валидны, нет слабого TLS | cert-manager metrics, testssl.sh, Alertmanager | TLS 1.3/1.2 strong only, сертификат не истекает в ближайшие 14 дней |
| **Data discovery** | Новые PII-файлы/таблицы найдены и размечены | Purview / OpenMetadata scanner | Объект с PII получает тег и owner |
| **Lineage control** | Понятно, откуда пришли данные и куда ушли | OpenMetadata | Любая аналитическая витрина имеет lineage до источника |
| **Analytics promotion gate** | В BI не публикуются raw PII/medical data | OpenMetadata + OPA | Витрина опубликована только с тегом `anonymized` или `aggregated` |
| **Vault audit** | Нет массовых decrypt/read secret операций | Vault audit + SIEM | Аномалия создаёт инцидент |
| **Access anomaly detection** | Нет нетипичного просмотра данных пациентских карт | Elastic/OpenSearch SIEM | Алерт при массовом доступе, доступе вне роли/филиала/графика |
| **Backup compliance** | Бэкапы зашифрованы и восстановимы | Backup audit, restore drills | Есть успешный restore test и ключи доступны через KMS |
| **DLP control** | Нет отправки ПДн наружу по почте/USB | DLP, EDR | Блокировка или карантин при попытке выгрузки |

## 2. Политики, которые должны быть автоматизированы

### 2.1. Запрет PII в логах

```yaml
policy: no_pii_in_logs
deny_fields:
  - full_name
  - birth_date
  - phone
  - email
  - diagnosis
  - chronic_conditions
  - lab_result
  - payment_details
action:
  ci: fail
  runtime: mask
```

### 2.2. Проверка API на BOLA/IDOR

```rego
package medikamente.privacy

default allow = false

allow {
  input.user.role == "patient"
  input.resource.patient_id == input.user.patient_id
  not contains(input.resource.tags, "pii.sensitive")
}

allow {
  input.user.role == "doctor"
  input.action in ["read", "write"]
  input.resource.patient_id in input.user.assigned_patient_ids
}

allow {
  input.user.role == "reception"
  input.action == "read"
  contains(input.resource.tags, "domain.appointment")
}
```

### 2.3. Запрет публикации аналитической витрины с PII

```yaml
policy: analytics_dataset_promotion
allow_publish_when:
  required_tags:
    - anonymized
  forbidden_tags:
    - pii
    - pii.sensitive
    - fin.raw
    - hr.raw
action:
  ci: fail
  catalog: block_promotion
```

### 2.4. Проверка шифрования хранилища

```yaml
policy: storage_encryption_required
resources:
  - postgres
  - minio_bucket
  - backup_repository
  - kubernetes_secret
required:
  encryption_at_rest: true
  key_source: vault_or_kms
  audit_enabled: true
```

## 3. Метрики и алерты

| Метрика | Источник | Порог | Реакция |
|---------|----------|-------|---------|
| `vault_decrypt_count{service}` | Vault audit | > baseline x3 за 15 минут | Security alert |
| `pii_access_count{user}` | API Gateway / OPA | > baseline x2 | Проверка аномалии |
| `medical_record_read_count{doctor}` | МИС audit | Доступ к пациенту вне назначения | Блокировка сессии |
| `tls_certificate_days_to_expire` | cert-manager | < 14 дней | Warning; < 3 дней Critical |
| `dlp_blocked_events` | DLP | > 0 | Инцидент ИБ |
| `unencrypted_storage_detected` | OPA/Purview | > 0 | Блокировка релиза / remediation |
| `backup_restore_success` | Backup audit | Нет успешного теста > 30 дней | Critical |
| `analytics_dataset_with_pii` | OpenMetadata | > 0 | Блокировка публикации витрины |

## 4. Процесс реакции

1. **Detect** — событие обнаруживается DLP/SIEM/Vault audit/OpenMetadata.
2. **Classify** — событие получает класс: `C3 PII`, `C4 Medical PII`, `C5 Financial`, `C7 Secrets`.
3. **Contain** — блокируется сессия, токен, сертификат или доступ к объекту.
4. **Investigate** — проверяются audit logs, lineage, пользователь, роль, источник запроса.
5. **Remediate** — ротация ключей/секретов, отзыв сертификатов, удаление копий, исправление политики.
6. **Report** — формируется отчёт для DPO/CTO; при необходимости запускается правовая процедура.

