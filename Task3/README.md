# Task3. Оценка Data Encryption at Rest and In Transit

## Состав решения

| Файл | Назначение |
|------|------------|
| `data-encryption-strategy.md` | Основная стратегия: классификация данных, обоснование защиты, инструменты at rest / in transit / in use |
| `protection-tools-register.md` | Реестр программных и аппаратных средств защиты данных |
| `automated-controls.md` | Автоматизированный контроль: CI/CD, DLP, SIEM, Vault audit, OpenMetadata, TLS monitoring |

## Краткая классификация

| Класс | Данные | Основная защита |
|-------|--------|-----------------|
| C1 Public | Публичная информация | TLS, контроль целостности |
| C2 Internal | Внутренние данные без ПДн | RBAC, шифрование дисков |
| C3 PII | ФИО, телефон, e-mail, адрес | AES-256, TLS, маскирование, аудит |
| C4 Sensitive Medical PII | Диагнозы, анализы, заключения | Field-level encryption, KMS/HSM, mTLS, ABAC, MFA |
| C5 Financial | Платежи, чеки, договоры | Токенизация, TLS/mTLS, аудит, шифрование |
| C6 HR | Кадровые и зарплатные данные | Отдельный HR-контур, AES-256, DLP |
| C7 Secrets | Пароли, API-ключи, TLS private keys | Vault/HSM, ротация, secret scanning |
| C8 Metadata | Имена файлов, audit trail, IP | Псевдонимизация, запрет PII в путях, log filtering |

## Основной вывод

Для «Медикаменте» максимальный приоритет имеют медицинские данные пациентов (`C4 Sensitive Medical PII`) и секреты (`C7 Secrets`). Их защита должна строиться не только на шифровании дисков, а на сквозной модели:

1. классификация и теги данных;
2. шифрование at rest через KMS/Vault;
3. TLS/mTLS для всех потоков in transit;
4. ABAC/RBAC через OPA;
5. запрет PII в логах и аналитике;
6. immutable audit и автоматические алерты.

