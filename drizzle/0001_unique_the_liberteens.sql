CREATE TABLE `analysis_answers` (
	`id` varchar(36) NOT NULL,
	`projectId` varchar(36) NOT NULL,
	`ownerId` int NOT NULL,
	`sourceDiagnosticId` varchar(36) NOT NULL,
	`questionId` varchar(36) NOT NULL,
	`answer` json NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `analysis_answers_id` PRIMARY KEY(`id`),
	CONSTRAINT `analysis_answers_source_question_uq` UNIQUE(`sourceDiagnosticId`,`questionId`)
);
--> statement-breakpoint
CREATE TABLE `analysis_diagnostics` (
	`id` varchar(36) NOT NULL,
	`projectId` varchar(36) NOT NULL,
	`ownerId` int NOT NULL,
	`fileId` varchar(36),
	`version` int NOT NULL,
	`status` enum('draft','completed_with_warnings','failed') NOT NULL,
	`contractVersion` varchar(64) NOT NULL,
	`engineVersion` varchar(64) NOT NULL,
	`rulesetVersion` varchar(64) NOT NULL,
	`payload` json NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `analysis_diagnostics_id` PRIMARY KEY(`id`),
	CONSTRAINT `analysis_diagnostics_project_owner_version_uq` UNIQUE(`projectId`,`ownerId`,`version`)
);
--> statement-breakpoint
CREATE TABLE `analysis_files` (
	`id` varchar(36) NOT NULL,
	`projectId` varchar(36) NOT NULL,
	`ownerId` int NOT NULL,
	`originalName` varchar(255) NOT NULL,
	`storageKey` text,
	`sha256` varchar(64) NOT NULL,
	`mimeType` varchar(160) NOT NULL,
	`sizeBytes` int NOT NULL,
	`sheetCount` int NOT NULL,
	`analyzableSheetCount` int NOT NULL,
	`retentionStatus` enum('private_active','reference_removed','rejected') NOT NULL DEFAULT 'private_active',
	`referenceRemovedAt` timestamp,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `analysis_files_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `analysis_projects` (
	`id` varchar(36) NOT NULL,
	`ownerId` int NOT NULL,
	`name` varchar(160) NOT NULL,
	`domain` varchar(80) NOT NULL DEFAULT 'generic',
	`status` enum('draft','uploading','analyzing','completed','failed') NOT NULL DEFAULT 'draft',
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	`completedAt` timestamp,
	CONSTRAINT `analysis_projects_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
ALTER TABLE `analysis_answers` ADD CONSTRAINT `analysis_answers_projectId_analysis_projects_id_fk` FOREIGN KEY (`projectId`) REFERENCES `analysis_projects`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_answers` ADD CONSTRAINT `analysis_answers_ownerId_users_id_fk` FOREIGN KEY (`ownerId`) REFERENCES `users`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_answers` ADD CONSTRAINT `analysis_answers_sourceDiagnosticId_analysis_diagnostics_id_fk` FOREIGN KEY (`sourceDiagnosticId`) REFERENCES `analysis_diagnostics`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_diagnostics` ADD CONSTRAINT `analysis_diagnostics_projectId_analysis_projects_id_fk` FOREIGN KEY (`projectId`) REFERENCES `analysis_projects`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_diagnostics` ADD CONSTRAINT `analysis_diagnostics_ownerId_users_id_fk` FOREIGN KEY (`ownerId`) REFERENCES `users`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_diagnostics` ADD CONSTRAINT `analysis_diagnostics_fileId_analysis_files_id_fk` FOREIGN KEY (`fileId`) REFERENCES `analysis_files`(`id`) ON DELETE set null ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_files` ADD CONSTRAINT `analysis_files_projectId_analysis_projects_id_fk` FOREIGN KEY (`projectId`) REFERENCES `analysis_projects`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_files` ADD CONSTRAINT `analysis_files_ownerId_users_id_fk` FOREIGN KEY (`ownerId`) REFERENCES `users`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE `analysis_projects` ADD CONSTRAINT `analysis_projects_ownerId_users_id_fk` FOREIGN KEY (`ownerId`) REFERENCES `users`(`id`) ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE INDEX `analysis_answers_owner_project_idx` ON `analysis_answers` (`ownerId`,`projectId`);--> statement-breakpoint
CREATE INDEX `analysis_diagnostics_owner_created_idx` ON `analysis_diagnostics` (`ownerId`,`createdAt`);--> statement-breakpoint
CREATE INDEX `analysis_files_project_owner_idx` ON `analysis_files` (`projectId`,`ownerId`);--> statement-breakpoint
CREATE INDEX `analysis_files_owner_retention_idx` ON `analysis_files` (`ownerId`,`retentionStatus`);--> statement-breakpoint
CREATE INDEX `analysis_projects_owner_status_idx` ON `analysis_projects` (`ownerId`,`status`);