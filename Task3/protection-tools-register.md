# Реестр программных и аппаратных средств защиты данных

## 1. Программные средства

| Средство | Тип | Назначение | Какие данные защищает | Где применяется |
|----------|-----|------------|------------------------|-----------------|
| **HashiCorp Vault** | KMS / Secrets Management | Хранение ключей шифрования, API-ключей, TLS private keys | C3 PII, C4 Medical PII, C5 Financial, C7 Secrets | Все сервисы, CI/CD, K8s |
| **HSM / CloudHSM / YubiHSM** | Аппаратный KMS | Защита master keys и операций подписи | C4, C5, C7 | Контур KMS/Vault |
| **PostgreSQL TDE / pgcrypto** | Шифрование БД | Шифрование таблиц/полей CRM и МИС | ПДн, медицинские данные, согласия | CRM, МИС, сервис записи |
| **MinIO / S3 SSE-KMS** | Объектное хранилище с шифрованием | Хранение PDF/JPG, заключений, договоров | Медицинские файлы, договоры | Файловый домен To-Be |
| **BitLocker / LUKS** | Шифрование дисков | Защита серверных дисков и переходных файловых зон | Все данные at rest на дисках | Windows/Linux серверы |
| **cert-manager** | Управление сертификатами | Выпуск и ротация TLS/mTLS сертификатов | Данные in transit | Kubernetes, API, service mesh |
| **Istio / Linkerd** | Service mesh | mTLS между сервисами, политики трафика | Все межсервисные потоки | Kubernetes |
| **Nginx / Kong / Envoy API Gateway** | API Gateway | TLS termination, rate limiting, field filtering | ПДн в API | Внешние и внутренние API |
| **Open Policy Agent (OPA)** | Policy Engine | RBAC/ABAC, BOLA/IDOR защита, policy-as-code | ПДн, медицинские данные, финансы | Gateway, сервисы, CI/CD |
| **OpenMetadata** | Каталог данных / lineage | Теги данных, lineage, контроль публикации витрин | Все классы данных | Data catalog, analytics |
| **Microsoft Purview Information Protection** | DLP / классификация | Сканирование Excel/PDF/JPG, авто-теги | Файлы As-Is и переходного периода | Windows Server, Exchange, файловое хранилище |
| **Elastic Stack / OpenSearch** | SIEM / аудит | Централизованный аудит, поиск аномалий | Логи доступа, события Vault/OPA | Security monitoring |
| **Victoria Metrics + Alertmanager** | Мониторинг | Метрики безопасности, алерты | События доступа, сертификаты, KMS | Observability |
| **Wazuh / OSSEC** | FIM / EDR-light | Контроль изменений файлов, аудит хостов | Файлы, конфиги, бэкапы | Серверы и рабочие станции |
| **Gitleaks / TruffleHog** | Secrets scanning | Поиск секретов в Git и CI | API-ключи, пароли, private keys | Репозитории, pipeline |
| **Semgrep** | SAST / privacy checks | Поиск логирования PII, небезопасных API | PII, medical PII | CI/CD |
| **OPA Conftest / Gatekeeper / Kyverno** | Policy-as-code | Проверка манифестов и контрактов | Конфигурации, secrets, API | CI/CD, Kubernetes |
| **DLP для почты и рабочих станций** | DLP | Запрет отправки PII/medical data наружу | ПДн, медданные, финансы | Exchange/Outlook, endpoints |
| **Backup encryption tool** | Шифрование бэкапов | Шифрование и проверка резервных копий | Все классы данных | Backup infrastructure |

## 2. Аппаратные и инфраструктурные средства

| Средство | Назначение | Какие риски снижает | Где применяется |
|----------|------------|---------------------|-----------------|
| **HSM** | Аппаратная защита master keys | Компрометация ключей шифрования | KMS/Vault |
| **TPM 2.0 на серверах** | Защита ключей полного шифрования диска | Кража физического сервера/диска | Windows/Linux серверы |
| **NGFW / межсетевой экран** | Сегментация сети и контроль потоков | Lateral movement, доступ из недоверенных зон | Между DMZ, app, data, legacy |
| **WAF** | Защита публичных API и порталов | OWASP Top 10, инъекции, атаки на API | Перед порталом пациента и API Gateway |
| **VPN / ZTNA Gateway** | Безопасный удалённый доступ сотрудников | Доступ из небезопасных сетей | Администраторы, удалённые филиалы |
| **PAM / Bastion host** | Контроль привилегированного доступа | Неконтролируемый доступ админов | Серверы, Vault, БД |
| **Immutable backup storage** | Защита резервных копий от удаления/шифровальщика | Ransomware, удаление бэкапов | Backup контур |
| **EDR на рабочих станциях** | Обнаружение вредоносного ПО и утечек | Инсайдеры, malware, копирование файлов | Рабочие места сотрудников |
| **Аппаратные MFA-ключи** | Усиленная аутентификация | Фишинг, захват учётки | Администраторы, врачи, бухгалтерия |

## 3. Соответствие средств классам данных

| Класс данных | Обязательные средства | Дополнительные средства |
|--------------|-----------------------|-------------------------|
| C1 Public | TLS, WAF | Контроль целостности |
| C2 Internal | TLS, RBAC, шифрование дисков | DLP, SIEM |
| C3 PII | TLS/mTLS, AES-256, Vault, OPA, аудит | DLP, Purview, tokenization |
| C4 Sensitive Medical PII | mTLS, field-level encryption, HSM/Vault, ABAC, MFA, immutable audit | DLP, PAM, dedicated storage, FIM |
| C5 Financial | TLS/mTLS, tokenization, Vault, аудит, сегментация | PCI DSS tooling, fraud monitoring |
| C6 HR | AES-256, RBAC, DLP, аудит | PAM, отдельный HR-контур |
| C7 Secrets | Vault/HSM, rotation, MFA, secret scanning | PAM, break-glass workflow |
| C8 Metadata | Псевдонимизация, маскирование, log filtering | Purview/OpenMetadata, retention controls |

## 4. Целевые стандарты конфигурации

| Область | Стандарт |
|---------|----------|
| TLS | TLS 1.3 для внешних API; TLS 1.2 допускается только для legacy при documented exception |
| Cipher suites | Только современные AEAD-наборы: AES-GCM / ChaCha20-Poly1305 |
| Сертификаты | Автоматическая ротация, срок не более 90 дней для внутренних mTLS сертификатов |
| Шифрование данных | AES-256-GCM или эквивалент; отдельные ключи по доменам данных |
| Хеширование паролей | Argon2id или bcrypt с актуальными параметрами |
| Бэкапы | Всегда encrypted at rest, отдельные ключи, immutable copy |
| Логи | PII denylist + allowlist structured logging; медицинские данные не логируются |
| Ключи | Ротация, аудит всех decrypt/sign операций, запрет экспорта master keys |

