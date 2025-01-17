# Тесты проекта

Данный файл описывает тесты, реализованные в проекте, и их цели.

## test_about_auth.py

1. test_about_api_require: Проверяет необходимость использования API-ключа для доступа к маршрутам `/about`.

## test_about_basic.py

1. test_get_about_empty: Проверяет получение ошибки при отсутствии описания проекта.
2. test_create_and_get_about: Проверяет создание описания проекта и его успешное получение.

## test_about_update.py

1. test_update_about: Проверяет успешное обновление описания проекта.
2. test_create_about_already_exists: Проверяет обработку ошибки при повторном создании описания проекта.

## test_files_auth.py

1. test_files_api_require: Проверяет авторизацию для маршрутов `/files/create`, `/files/update`, `/files/delete` и `/files/read` при отсутствии API-ключа.

## test_files_create.py

1. test_create_file_missing_filename: Проверяет ошибку при попытке создать файл без указания имени.
2. test_create_file_success: Проверяет успешное создание файла с переданными параметрами.

## test_files_delete.py

1. test_delete_file: Проверяет успешное удаление существующего файла.
2. test_delete_file_nonexistent: Проверяет обработку ошибки при удалении несуществующего файла.
3. test_delete_file_not_in_db: Проверяет удаление файла, который отсутствует в базе данных, но существует физически.
4. test_delete_directory_success: Проверяет успешное рекурсивное удаление директории и всех её файлов.
5. test_delete_directory_nonexistent: Проверяет обработку ошибки при удалении несуществующей директории.

## test_files_read.py

1. test_read_file_success: Проверяет успешное чтение существующего файла, включая содержимое, размер и дату последнего изменения.
2. test_read_file_missing_filename: Проверяет ошибку при попытке чтения файла без указания имени.
3. test_read_file_nonexistent: Проверяет обработку ошибки при попытке чтения несуществующего файла.

## test_files_tree.py

1. test_tree_no_path: Проверяет генерацию дерева файлов без указания пути.
2. test_tree_with_valid_path: Проверяет генерацию дерева файлов для указанного пути.
3. test_tree_invalid_path: Проверяет обработку ошибки для несуществующего пути.
4. test_tree_with_depth: Проверяет ограничение глубины анализа структуры.
5. test_tree_with_excluded_dirs: Проверяет исключение указанных директорий из результата.
6. test_tree_with_excluded_patterns: Проверяет исключение директорий по паттернам, таких как `__pycache__`.

## test_files_update.py

1. test_update_file_content_success: Проверяет успешное обновление содержимого файла и описания.
2. test_update_file_content_nonexistent: Проверяет обработку ошибки при обновлении несуществующего файла.
3. test_update_file_without_content: Проверяет обновление только описания файла без изменения содержимого.
4. test_update_file_info_only: Проверяет обновление только описания файла с сохранением его содержимого неизменным.

## test_history_auth.py

1. test_history_api_require: Проверяет авторизацию для маршрутов `/history`, включая просмотр и добавление записей.

## test_history_file.py

1. test_missing_history_file: Проверяет попытку получить историю при отсутствии файла истории.
2. test_empty_history_file_with_content: Проверяет попытку получить историю из пустого файла истории.

## test_history_logging.py

1. test_log_and_get_history: Проверяет логирование изменений и их успешное получение через маршруты `/history`.
2. test_invalid_log_entry: Проверяет обработку ошибок при логировании с некорректными данными.
3. test_log_updates_project_description: Проверяет обновление поля `updated_at` в `project_description.json` при логировании изменений.

## test_privacy.py

1. test_privacy_policy_default: Проверяет отображение политики конфиденциальности по умолчанию (английский язык).
2. test_privacy_policy_russian: Проверяет отображение политики конфиденциальности на русском языке.
3. test_privacy_policy_german: Проверяет отображение политики конфиденциальности на немецком языке.
4. test_privacy_policy_french: Проверяет отображение политики конфиденциальности на французском языке.
5. test_privacy_policy_chinese: Проверяет отображение политики конфиденциальности на китайском языке.
6. test_privacy_policy_invalid_language: Проверяет обработку недопустимого языка (по умолчанию — английский).
7. test_privacy_api_require: Проверяет необходимость использования API-ключа для маршрута `/privacy`.

## test_project_map_auth.py

1. test_projectmap_api_require: Проверяет авторизацию для маршрутов карты проекта, включая добавление, удаление и синхронизацию файлов.

## test_project_map_basic.py

1. test_add_and_get_project_map: Проверяет добавление файла и успешное получение карты проекта.
2. test_delete_from_project_map: Проверяет удаление файла из карты проекта.
3. test_update_project_map: Проверяет обновление записи в карте проекта.

## test_project_map_errors.py

1. test_invalid_delete_request: Проверяет обработку ошибки при попытке удалить файл из карты проекта без указания пути.
2. test_invalid_update_request: Проверяет обработку ошибки при попытке обновить файл с некорректными данными.

## test_project_map_sync.py

1. test_sync_project_files: Проверяет синхронизацию файлов с картой проекта, включая обработку несуществующих файлов.
2. test_sync_file_already_in_db: Проверяет обработку повторной синхронизации файла, уже существующего в базе данных.