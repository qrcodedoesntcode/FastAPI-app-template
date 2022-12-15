BEGIN;

INSERT INTO cre_permission (id, scope, description) VALUES
        (1, 'admin', 'Admin permissions: can do everything'),
        (2, 'role:read', 'Role permissions: can read all roles and specific user roles'),
        (3, 'role:create', 'Role permissions: can create roles'),
        (4, 'role:delete', 'Role permissions: can delete roles'),
        (5, 'role:link', 'Role permissions: can link/unlink roles to users'),
        (6, 'permission:read', 'Permission permissions: can read all permissions and specific user permissions'),
        (7, 'permission:create', 'Permission permissions: can create permissions'),
        (8, 'permission:delete', 'Permission permissions: can delete permissions'),
        (9, 'permission:link', 'Permission permissions: can link/unlink permissions to roles');


-- Password: password
INSERT INTO cre_user (id, username, email, password, is_active) VALUES
        (1, 'admin', 'admin@example.com', '$2b$12$cD.5A3wFiV0JFW3lb9tJyeSYHwvfyYZ2TI18KrgJWaLCGSBVgitcO', true),
        (2, 'admin_roles', 'admin_roles@example.com', '$2b$12$wy07LPR0EBugLLEUUu8UMObJEftygls5Ax.AIxX0hVGihT6KyW1Yy', true),
        (3, 'admin_permissions', 'admin_permissions@example.com', '$2b$12$TXMeCKv7m/g5HYvhCTl5V.f9tiMTFMwZTT3nQ3VqmO5mJYOV53qoe', true);


INSERT INTO cre_profile (id, line1, line2, city, province, postcode, user_id) VALUES
        (1, NULL, NULL, NULL, NULL, NULL, 1),
        (2, NULL, NULL, NULL, NULL, NULL, 2),
        (3, NULL, NULL, NULL, NULL, NULL, 3);


INSERT INTO cre_role (id, name, description) VALUES
        (1, 'Administrator', 'Can do everything'),
        (3, 'Permissions Admin', 'Can do everything related to permissions (read/write/delete/link/unlink)'),
        (2, 'Roles Admin', 'Can do everything related to roles (read/write/delete/link/unlink)');


INSERT INTO cre_role_permission (cre_role_id, cre_permission_id) VALUES
        (1, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 9);


INSERT INTO cre_user_role (cre_user_id, cre_role_id) VALUES
        (1, 1),
        (2, 2),
        (3, 3);

COMMIT;
