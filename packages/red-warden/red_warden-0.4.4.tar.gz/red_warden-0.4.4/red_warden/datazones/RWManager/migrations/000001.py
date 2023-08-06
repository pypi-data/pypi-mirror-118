import json
from red_warden.config import RWConfig
from red_warden.datalayer import RWMysqlBackend
from red_warden.helpers import import_string
from red_warden.enums import RWBackendDestinationEnum


async def upgrade(db):
    async with RWMysqlBackend(
        RWConfig["RW_BACKEND_ENDPOINTS"],
        {
            "username": RWConfig["RW_BACKEND_USERNAME"],
            "password": RWConfig["RW_BACKEND_PASSWORD"],
        },
    ) as _db:
        # check if database exists, else creates it
        db_exists = await _db.fetch_val(
            "SHOW DATABASES LIKE :db_name", {"db_name": RWConfig["RW_BACKEND_DB_NAME"]}
        )
        if not db_exists:
            await _db.execute(
                "CREATE DATABASE %s DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
                % RWConfig["RW_BACKEND_DB_NAME"]
            )

            # ensure all grants are set for this user to the Manager database and tables
            await _db.execute(
                "GRANT ALL ON %s.* TO :username@'%%'" % RWConfig["RW_BACKEND_DB_NAME"],
                {"username": RWConfig["RW_BACKEND_USERNAME"]},
            )

    async with db:
        await db.execute(
            """        
            CREATE TABLE `backend` (
              `id` binary(16) NOT NULL,
              `name` varchar(250) NOT NULL,
              `type` enum('mysql','mongodb','redis') NOT NULL,
              `destination` enum('global', 'tenants_available', 'tenants_full') NOT NULL,
              `params` varchar(250) DEFAULT NULL,
              `endpoints` varchar(250) NOT NULL,
              `enabled` enum('Y','N') NOT NULL DEFAULT 'N',
              PRIMARY KEY (`id`),
              UNIQUE KEY `backend_name_uindex` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `tenant` (
              `id` binary(16) NOT NULL,
              `name` varchar(250) NOT NULL,
              `params` varchar(250) DEFAULT NULL,
              `enabled` enum('Y','N') NOT NULL DEFAULT 'N',
              PRIMARY KEY (`id`),
              UNIQUE KEY `tenant_name_uindex` (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `datapath` (
              `id` binary(16) NOT NULL,
              `tenant_id` binary(16) DEFAULT NULL,
              `datazone` varchar(250) NOT NULL,
              `backend_id` binary(16) NOT NULL,
              `db_name` varchar(100) DEFAULT NULL,
              `version` bigint NOT NULL,
              PRIMARY KEY (`id`),
              KEY `datapath_backend_id_fk` (`backend_id`),
              KEY `datapath_tenant_id_fk` (`tenant_id`),
              CONSTRAINT `datapath_backend_id_fk` FOREIGN KEY (`backend_id`) REFERENCES `backend` (`id`) ON DELETE CASCADE,
              CONSTRAINT `datapath_tenant_id_fk` FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `key` (
              `id` binary(16) NOT NULL,
              `login` varchar(250) NOT NULL,
              `password_hash` varchar(250) NOT NULL,
              `enabled` enum('Y','N') NOT NULL DEFAULT 'N',
              `mfa_enabled` enum('Y','N') NOT NULL DEFAULT 'N',
              `mfa_secret` varchar(250) DEFAULT NULL,
              PRIMARY KEY (`id`),
              UNIQUE KEY `key_login_uindex` (`login`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `session` (
              `id` binary(16) NOT NULL,
              `key` varchar(50) NOT NULL,
              `value` varchar(2048) NOT NULL,
              `expires_at` datetime NOT NULL,
              `key_id` binary(16) DEFAULT NULL,
              PRIMARY KEY (`id`),
              KEY `session_key_id_fk` (`key_id`),
              CONSTRAINT `session_key_id_fk` FOREIGN KEY (`key_id`) REFERENCES `key` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `oauth2_client` (
              `id` binary(16) NOT NULL,
              `name` varchar(150) NOT NULL,
              `secret` varchar(150) NOT NULL,
              `grant_types` varchar(150) DEFAULT NULL,
              `response_types` varchar(150) NOT NULL,
              `redirect_uris` varchar(500) NOT NULL,
              `scope` varchar(150) DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `oauth2_authorization_code` (
              `id` binary(16) NOT NULL,
              `code` varchar(250) NOT NULL,
              `oauth2_client_id` binary(16) NOT NULL,
              `key_id` binary(16) NOT NULL,
              `redirect_uri` varchar(150) NOT NULL,
              `response_type` varchar(150) NOT NULL,
              `scope` varchar(150) DEFAULT NULL,
              `auth_time` datetime NOT NULL,
              `expires_in` bigint DEFAULT NULL,
              `nonce` varchar(150) DEFAULT NULL,
              `code_challenge` varchar(150) NOT NULL,
              `code_challenge_method` varchar(10) DEFAULT NULL,
              PRIMARY KEY (`id`),
              KEY `oauth2_authorization_code_oauth2_client_id_fk` (`oauth2_client_id`),
              KEY `oauth2_authorization_code_key_id_fk` (`key_id`),
              CONSTRAINT `oauth2_authorization_code_key_id_fk` FOREIGN KEY (`key_id`) REFERENCES `key` (`id`) ON DELETE CASCADE,
              CONSTRAINT `oauth2_authorization_code_oauth2_client_id_fk` FOREIGN KEY (`oauth2_client_id`) REFERENCES `oauth2_client` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `oauth2_token` (
              `id` binary(16) NOT NULL,
              `access_token` varchar(250) NOT NULL,
              `refresh_token` varchar(250) DEFAULT NULL,
              `scope` varchar(250) DEFAULT NULL,
              `issued_at` DATETIME NOT NULL,
              `access_token_expires_in` INT NOT NULL,
              `refresh_token_expires_in` INT NOT NULL,
              `oauth2_client_id` binary(16) NOT NULL,
              `key_id` binary(16) DEFAULT NULL,
              `token_type` varchar(50) NOT NULL,
              `revoked` enum('Y','N') NOT NULL DEFAULT 'N',
              PRIMARY KEY (`id`),
              KEY `oauth2_token_oauth2_client_id_fk` (`oauth2_client_id`),
              KEY `oauth2_token_key_id_fk` (`key_id`),
              CONSTRAINT `oauth2_token_key_id_fk` FOREIGN KEY (`key_id`) REFERENCES `key` (`id`) ON DELETE CASCADE,
              CONSTRAINT `oauth2_token_oauth2_client_id_fk` FOREIGN KEY (`oauth2_client_id`) REFERENCES `oauth2_client` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `acl_role` (
              `id` binary(16) NOT NULL,
              `name` varchar(250) NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `acl_permission` (
              `id` binary(16) NOT NULL,
              `name` varchar(250) NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `acl_role_permission_link` (
              `id` binary(16) NOT NULL,
              `acl_role_id` binary(16) NOT NULL,
              `acl_permission_id` binary(16) NOT NULL,
              KEY `acl_role_permission_link_acl_permission_id_fk` (`acl_permission_id`),
              KEY `acl_role_permission_link_acl_role_id_fk` (`acl_role_id`),
              CONSTRAINT `acl_role_permission_link_acl_permission_id_fk` FOREIGN KEY (`acl_permission_id`) REFERENCES `acl_permission` (`id`) ON DELETE CASCADE,
              CONSTRAINT `acl_role_permission_link_acl_role_id_fk` FOREIGN KEY (`acl_role_id`) REFERENCES `acl_role` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            
            CREATE TABLE `acl_role_key_link` (
              `id` binary(16) NOT NULL,
              `acl_role_id` binary(16) NOT NULL,
              `key_id` binary(16) NOT NULL,
              PRIMARY KEY (`id`),
              KEY `acl_role_key_link_acl_role_id_fk` (`acl_role_id`),
              KEY `acl_role_key_link_key_id_fk` (`key_id`),
              CONSTRAINT `acl_role_key_link_acl_role_id_fk` FOREIGN KEY (`acl_role_id`) REFERENCES `acl_role` (`id`) ON DELETE CASCADE,
              CONSTRAINT `acl_role_key_link_key_id_fk` FOREIGN KEY (`key_id`) REFERENCES `key` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    
        """
        )

        # inserts the main "Red Warden" key, password "RED_WARDEN"
        model = import_string("red_warden.datazones.RWManager.RWKeyModel")
        key = await model.before_create(
            db,
            {"login": "Red Warden", "enabled": "Y", "password": "RED_WARDEN"},
            skip_validation=True,
        )
        await db.execute(model.insert().values(key))

        # inserts the main OAuth2 client
        model = import_string("red_warden.datazones.RWManager.RWOAuth2ClientModel")
        oauth2_client = await model.before_create(
            db,
            {
                "name": "red_warden_oauth2_client",
                "secret": "RED_WARDEN",
                "grant_types": "authorization_code,password",
                "response_types": "code,token",
                "redirect_uris": "",
                "scope": "manager",
            },
            skip_validation=True,
        )
        await db.execute(model.insert().values(oauth2_client))

        # inserts the global backend
        model = import_string("red_warden.datazones.RWManager.RWBackendModel")
        backend = await model.before_create(
            db,
            {
                "name": "rw_global",
                "destination": RWBackendDestinationEnum.GLOBAL,
                "type": "mysql",
                "params": json.dumps(db.params),
                "endpoints": RWConfig["RW_BACKEND_ENDPOINTS"],
                "enabled": "Y",
            },
            skip_validation=True,
        )
        await db.execute(model.insert().values(backend))


# CREATE TABLE ___RED_WARDEN_MANAGER_DB___.`history` (
#   `id` binary(16) NOT NULL,
#   `record_id` varchar(250) NOT NULL,
#   `who` varchar(250) NOT NULL,
#   `why` enum('INSERT','UPDATE','DELETE') NOT NULL,
#   `what` json NOT NULL,
#   `when` datetime NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
