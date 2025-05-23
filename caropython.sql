-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: caropython
-- ------------------------------------------------------
-- Server version	8.4.5

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `avatar`
--

DROP TABLE IF EXISTS `avatar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `avatar` (
  `avatar_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price` int DEFAULT '0',
  PRIMARY KEY (`avatar_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `avatar`
--

LOCK TABLES `avatar` WRITE;
/*!40000 ALTER TABLE `avatar` DISABLE KEYS */;
INSERT INTO `avatar` VALUES (1,'Man1','https://static.vecteezy.com/system/resources/previews/011/459/666/original/people-avatar-icon-png.png',100),(2,'Woman1','https://cdn2.iconfinder.com/data/icons/circle-avatars-1/128/040_girl_avatar_profile_woman_kimono_flower-1024.png',100);
/*!40000 ALTER TABLE `avatar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `games` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `room_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `player1_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `player2_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `winner_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'ongoing',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `current_player_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `room_code` (`room_code`),
  KEY `idx_status` (`status`),
  KEY `fk_games_player1` (`player1_id`),
  KEY `fk_games_player2` (`player2_id`),
  KEY `fk_games_winner` (`winner_id`),
  KEY `fk_current_player` (`current_player_id`),
  CONSTRAINT `fk_current_player` FOREIGN KEY (`current_player_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_games_player1` FOREIGN KEY (`player1_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL,
  CONSTRAINT `fk_games_player2` FOREIGN KEY (`player2_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL,
  CONSTRAINT `fk_games_winner` FOREIGN KEY (`winner_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games`
--

LOCK TABLES `games` WRITE;
/*!40000 ALTER TABLE `games` DISABLE KEYS */;
INSERT INTO `games` VALUES (1,'pve_638583','rvoIUFcCVU',NULL,'rvoIUFcCVU','finished','2025-05-21 04:59:43',NULL),(2,'769036','rvoIUFcCVU','QWKAIzKOga',NULL,'ongoing','2025-05-21 04:59:59',NULL),(3,'pve_678835','rvoIUFcCVU',NULL,'rvoIUFcCVU','finished','2025-05-21 08:02:42',NULL),(4,'pve_788456','rvoIUFcCVU',NULL,NULL,'ongoing','2025-05-21 08:02:56',NULL),(5,'pve_439073','rvoIUFcCVU',NULL,NULL,'finished','2025-05-21 08:28:40',NULL),(6,'875188','rvoIUFcCVU',NULL,NULL,'ongoing','2025-05-21 08:28:50',NULL),(7,'114819','rvoIUFcCVU',NULL,NULL,'waiting','2025-05-21 08:39:17',NULL),(8,'243381','rvoIUFcCVU',NULL,NULL,'waiting','2025-05-21 08:43:13',NULL),(9,'927000','rvoIUFcCVU','iQvDlyRt8q',NULL,'ongoing','2025-05-21 08:46:00',NULL),(10,'684718','rvoIUFcCVU','BnDC8QsRDy',NULL,'ongoing','2025-05-21 08:48:37',NULL),(11,'021429','V1HcHSAmil','BnDC8QsRDy',NULL,'ongoing','2025-05-21 08:56:28',NULL),(12,'125633','BnDC8QsRDy',NULL,NULL,'waiting','2025-05-21 08:56:51',NULL),(13,'482135','V1HcHSAmil','w4UOvX1Gka',NULL,'ongoing','2025-05-21 09:01:05',NULL),(14,'509126','w4UOvX1Gka',NULL,NULL,'waiting','2025-05-21 09:01:33',NULL),(15,'046742','V1HcHSAmil','Y1ChbRPST0',NULL,'ongoing','2025-05-21 09:03:19',NULL),(16,'204932','QWKAIzKOga','7cbkmeVKwi',NULL,'ongoing','2025-05-21 09:06:36','QWKAIzKOga'),(17,'412972','V1HcHSAmil','hoXRVjYibG','V1HcHSAmil','finished','2025-05-21 09:16:30','hoXRVjYibG'),(18,'717858','V1HcHSAmil','NqtK6ESkOT','NqtK6ESkOT','finished','2025-05-21 09:19:49','V1HcHSAmil'),(19,'331380','V1HcHSAmil','uH2v1nVcql','V1HcHSAmil','finished','2025-05-21 09:24:08','uH2v1nVcql'),(20,'339788','V1HcHSAmil','eItlm5OB3J','V1HcHSAmil','finished','2025-05-21 09:29:46','eItlm5OB3J'),(21,'410488','eItlm5OB3J',NULL,NULL,'waiting','2025-05-21 09:30:00',NULL),(22,'785036','QWKAIzKOga','WrEQtzKEqd','QWKAIzKOga','finished','2025-05-21 09:32:42','WrEQtzKEqd'),(23,'203830','QWKAIzKOga','JlZ4fbzQLX','JlZ4fbzQLX','finished','2025-05-21 09:34:18','QWKAIzKOga'),(24,'770793','QWKAIzKOga','JlZ4fbzQLX',NULL,'ongoing','2025-05-21 09:40:38',NULL),(25,'453486','QWKAIzKOga','JlZ4fbzQLX',NULL,'ongoing','2025-05-21 09:45:37',NULL),(26,'066449','QWKAIzKOga','JlZ4fbzQLX',NULL,'ongoing','2025-05-21 09:48:12',NULL),(27,'651942','QWKAIzKOga','JlZ4fbzQLX','QWKAIzKOga','finished','2025-05-21 09:52:17','QWKAIzKOga'),(28,'123559','QWKAIzKOga','JlZ4fbzQLX','JlZ4fbzQLX','finished','2025-05-21 09:54:43','QWKAIzKOga'),(29,'pve_476725','V1HcHSAmil',NULL,NULL,'finished','2025-05-21 09:59:03',NULL),(30,'126799','V1HcHSAmil',NULL,NULL,'waiting','2025-05-23 01:07:06','V1HcHSAmil'),(31,'025377','QllQ2mn7V4','IV9Dz4f08o',NULL,'ongoing','2025-05-23 01:08:30','QllQ2mn7V4'),(32,'919682','V1HcHSAmil','MSajhWI46m',NULL,'ongoing','2025-05-23 01:10:29','V1HcHSAmil'),(33,'780834','MSajhWI46m',NULL,NULL,'waiting','2025-05-23 01:10:49','MSajhWI46m'),(34,'713963','QWKAIzKOga','dYRS4kFOF6',NULL,'ongoing','2025-05-23 01:16:36',NULL),(35,'pve_807540','V1HcHSAmil',NULL,NULL,'ongoing','2025-05-23 01:27:10',NULL),(36,'pve_964389','V1HcHSAmil',NULL,NULL,'ongoing','2025-05-23 01:34:27',NULL),(37,'944739','V1HcHSAmil','xwG8m8BeVL','xwG8m8BeVL','finished','2025-05-23 01:38:53','V1HcHSAmil'),(38,'236712','V1HcHSAmil',NULL,NULL,'waiting','2025-05-23 01:40:00','V1HcHSAmil'),(39,'868827','V1HcHSAmil',NULL,NULL,'waiting','2025-05-23 01:47:33','V1HcHSAmil'),(40,'444968','V1HcHSAmil','fFfQPgSKdz','V1HcHSAmil','finished','2025-05-23 01:48:03','V1HcHSAmil'),(41,'pve_883432','V1HcHSAmil',NULL,'V1HcHSAmil','finished','2025-05-23 01:48:58',NULL),(42,'105518','V8Oc012oA1','vdlLAOQ4Op','V8Oc012oA1','finished','2025-05-23 02:04:46','V8Oc012oA1'),(43,'263558','G3oEf0cceX',NULL,NULL,'waiting','2025-05-23 02:08:34','G3oEf0cceX'),(44,'pve_696011','vdlLAOQ4Op',NULL,'vdlLAOQ4Op','finished','2025-05-23 02:11:52',NULL),(45,'023989','vdlLAOQ4Op',NULL,NULL,'waiting','2025-05-23 02:12:31','vdlLAOQ4Op'),(46,'896395','V8Oc012oA1',NULL,NULL,'waiting','2025-05-23 02:13:02','V8Oc012oA1'),(47,'757626','G3oEf0cceX','RFL1Naoe34','RFL1Naoe34','finished','2025-05-23 02:14:03','RFL1Naoe34'),(48,'040266','G3oEf0cceX','RFL1Naoe34','RFL1Naoe34','finished','2025-05-23 02:23:58','RFL1Naoe34'),(49,'839358','G3oEf0cceX','RFL1Naoe34','G3oEf0cceX','finished','2025-05-23 02:29:06','G3oEf0cceX'),(50,'pve_399778','G3oEf0cceX',NULL,NULL,'finished','2025-05-23 02:30:12',NULL),(51,'886957','RFL1Naoe34','G3oEf0cceX','RFL1Naoe34','finished','2025-05-23 02:34:29','RFL1Naoe34'),(52,'874397','G3oEf0cceX','RFL1Naoe34','G3oEf0cceX','finished','2025-05-23 02:43:05','G3oEf0cceX'),(53,'207783','G3oEf0cceX','RFL1Naoe34','RFL1Naoe34','finished','2025-05-23 02:51:38','G3oEf0cceX'),(54,'577575','RFL1Naoe34',NULL,NULL,'waiting','2025-05-23 02:52:00','RFL1Naoe34'),(55,'230357','G3oEf0cceX','RFL1Naoe34','G3oEf0cceX','finished','2025-05-23 02:55:29','RFL1Naoe34'),(56,'863849','G3oEf0cceX','RFL1Naoe34','G3oEf0cceX','finished','2025-05-23 03:04:14','G3oEf0cceX'),(57,'043037','G3oEf0cceX','RFL1Naoe34','RFL1Naoe34','finished','2025-05-23 03:08:47','G3oEf0cceX'),(58,'815608','G3oEf0cceX','RFL1Naoe34','RFL1Naoe34','finished','2025-05-23 03:09:36','G3oEf0cceX');
/*!40000 ALTER TABLE `games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leaderboard`
--

DROP TABLE IF EXISTS `leaderboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaderboard` (
  `rank_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `wins` int DEFAULT '0',
  `losses` int DEFAULT '0',
  `total_games` int DEFAULT '0',
  `win_rate` float DEFAULT '0',
  PRIMARY KEY (`rank_id`),
  KEY `user_id` (`user_id`),
  KEY `idx_wins` (`wins`),
  CONSTRAINT `fk_leaderboard_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leaderboard`
--

LOCK TABLES `leaderboard` WRITE;
/*!40000 ALTER TABLE `leaderboard` DISABLE KEYS */;
INSERT INTO `leaderboard` VALUES (21,'user1',40,0,0,0),(22,'user2',23,0,0,0),(23,'user3',19,0,0,0),(24,'user4',64,0,0,0),(25,'user5',47,0,0,0),(26,'user6',67,0,0,0),(27,'user7',74,0,0,0),(28,'user8',50,0,0,0),(29,'user9',43,0,0,0),(30,'user10',40,0,0,0),(31,'user11',7,0,0,0),(32,'user12',93,0,0,0),(33,'user13',6,0,0,0),(34,'user14',92,0,0,0),(35,'user15',85,0,0,0),(36,'user16',88,0,0,0),(37,'user17',58,0,0,0),(38,'user18',97,0,0,0),(39,'user19',98,0,0,0),(40,'user20',72,0,0,0),(41,'QWKAIzKOga',1,1,2,50),(42,'JlZ4fbzQLX',1,1,2,50),(43,'xwG8m8BeVL',1,0,1,100),(44,'V1HcHSAmil',1,1,2,50),(45,'fFfQPgSKdz',0,1,1,0),(46,'V8Oc012oA1',1,0,1,100),(47,'vdlLAOQ4Op',0,1,1,0),(48,'RFL1Naoe34',6,4,10,60),(49,'G3oEf0cceX',4,6,10,40);
/*!40000 ALTER TABLE `leaderboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `move`
--

DROP TABLE IF EXISTS `move`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `move` (
  `move_id` int NOT NULL AUTO_INCREMENT,
  `game_id` int DEFAULT NULL,
  `player_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `position` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `move_order` int DEFAULT '0',
  `position_x` int DEFAULT NULL,
  `position_y` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`move_id`),
  KEY `game_id` (`game_id`),
  KEY `player_id` (`player_id`),
  KEY `idx_move_order` (`move_order`),
  CONSTRAINT `fk_move_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_move_player` FOREIGN KEY (`player_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=185 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `move`
--

LOCK TABLES `move` WRITE;
/*!40000 ALTER TABLE `move` DISABLE KEYS */;
INSERT INTO `move` VALUES (1,11,'BnDC8QsRDy','9,2',1,9,2,'2025-05-21 15:57:15'),(2,11,'BnDC8QsRDy','7,2',2,7,2,'2025-05-21 15:57:18'),(3,11,'BnDC8QsRDy','8,3',3,8,3,'2025-05-21 15:57:22'),(4,11,'BnDC8QsRDy','9,3',4,9,3,'2025-05-21 15:57:23'),(5,11,'V1HcHSAmil','3,4',5,3,4,'2025-05-21 15:57:39'),(6,11,'V1HcHSAmil','0,0',6,0,0,'2025-05-21 15:57:40'),(7,11,'V1HcHSAmil','1,0',7,1,0,'2025-05-21 15:57:40'),(8,11,'V1HcHSAmil','6,0',8,6,0,'2025-05-21 15:57:43'),(9,11,'V1HcHSAmil','11,0',9,11,0,'2025-05-21 15:57:43'),(10,11,'V1HcHSAmil','13,0',10,13,0,'2025-05-21 15:57:43'),(11,11,'V1HcHSAmil','12,0',11,12,0,'2025-05-21 15:57:44'),(12,11,'V1HcHSAmil','14,0',12,14,0,'2025-05-21 15:57:44'),(13,11,'V1HcHSAmil','5,8',13,5,8,'2025-05-21 15:58:09'),(14,11,'V1HcHSAmil','9,8',14,9,8,'2025-05-21 15:58:30'),(15,11,'V1HcHSAmil','6,7',15,6,7,'2025-05-21 15:58:35'),(16,13,'w4UOvX1Gka','6,3',1,6,3,'2025-05-21 16:01:41'),(17,13,'V1HcHSAmil','6,5',2,6,5,'2025-05-21 16:01:43'),(18,13,'w4UOvX1Gka','8,5',3,8,5,'2025-05-21 16:01:46'),(19,13,'w4UOvX1Gka','7,5',4,7,5,'2025-05-21 16:01:46'),(20,13,'w4UOvX1Gka','9,5',5,9,5,'2025-05-21 16:01:47'),(21,13,'w4UOvX1Gka','8,4',6,8,4,'2025-05-21 16:01:48'),(22,13,'w4UOvX1Gka','8,9',7,8,9,'2025-05-21 16:02:02'),(23,13,'V1HcHSAmil','10,3',8,10,3,'2025-05-21 16:02:17'),(24,13,'V1HcHSAmil','9,4',9,9,4,'2025-05-21 16:02:19'),(25,13,'V1HcHSAmil','9,4',9,9,4,'2025-05-21 16:02:19'),(26,13,'w4UOvX1Gka','10,4',10,10,4,'2025-05-21 16:02:21'),(27,13,'w4UOvX1Gka','9,6',11,9,6,'2025-05-21 16:02:21'),(28,13,'V1HcHSAmil','7,7',12,7,7,'2025-05-21 16:02:23'),(29,13,'V1HcHSAmil','13,0',13,13,0,'2025-05-21 16:02:23'),(30,13,'V1HcHSAmil','14,0',14,14,0,'2025-05-21 16:02:24'),(31,15,'Y1ChbRPST0','8,5',1,8,5,'2025-05-21 16:03:47'),(32,15,'V1HcHSAmil','7,3',2,7,3,'2025-05-21 16:03:52'),(33,15,'Y1ChbRPST0','8,2',3,8,2,'2025-05-21 16:05:54'),(34,15,'Y1ChbRPST0','8,3',4,8,3,'2025-05-21 16:06:01'),(35,15,'Y1ChbRPST0','9,5',5,9,5,'2025-05-21 16:06:02'),(36,15,'Y1ChbRPST0','9,3',6,9,3,'2025-05-21 16:06:03'),(37,16,'7cbkmeVKwi','4,1',1,4,1,'2025-05-21 16:07:24'),(38,16,'7cbkmeVKwi','7,3',2,7,3,'2025-05-21 16:07:32'),(39,16,'7cbkmeVKwi','10,4',3,10,4,'2025-05-21 16:16:05'),(40,17,'hoXRVjYibG','5,4',1,5,4,'2025-05-21 16:16:56'),(41,17,'hoXRVjYibG','8,3',2,8,3,'2025-05-21 16:17:12'),(42,17,'V1HcHSAmil','5,3',3,5,3,'2025-05-21 16:17:31'),(43,17,'V1HcHSAmil','7,6',4,7,6,'2025-05-21 16:17:41'),(44,17,'V1HcHSAmil','7,4',5,7,4,'2025-05-21 16:17:49'),(45,17,'V1HcHSAmil','6,4',6,6,4,'2025-05-21 16:17:53'),(46,18,'NqtK6ESkOT','6,5',1,6,5,'2025-05-21 16:20:10'),(47,19,'uH2v1nVcql','6,4',1,6,4,'2025-05-21 16:24:39'),(48,19,'uH2v1nVcql','10,7',2,10,7,'2025-05-21 16:25:02'),(49,19,'V1HcHSAmil','7,4',3,7,4,'2025-05-21 16:25:06'),(50,19,'V1HcHSAmil','8,4',4,8,4,'2025-05-21 16:25:32'),(51,19,'V1HcHSAmil','8,5',5,8,5,'2025-05-21 16:25:32'),(52,19,'V1HcHSAmil','7,5',6,7,5,'2025-05-21 16:25:34'),(53,19,'V1HcHSAmil','9,4',7,9,4,'2025-05-21 16:25:36'),(54,19,'V1HcHSAmil','9,3',8,9,3,'2025-05-21 16:25:37'),(55,19,'V1HcHSAmil','12,4',9,12,4,'2025-05-21 16:25:38'),(56,19,'V1HcHSAmil','11,7',10,11,7,'2025-05-21 16:25:54'),(57,19,'V1HcHSAmil','13,5',11,13,5,'2025-05-21 16:25:57'),(58,20,'eItlm5OB3J','6,4',1,6,4,'2025-05-21 16:30:01'),(59,20,'V1HcHSAmil','7,4',2,7,4,'2025-05-21 16:30:03'),(60,20,'V1HcHSAmil','10,4',3,10,4,'2025-05-21 16:30:08'),(61,22,'QWKAIzKOga','7,4',1,7,4,'2025-05-21 16:33:12'),(62,22,'WrEQtzKEqd','8,5',2,8,5,'2025-05-21 16:33:16'),(63,22,'QWKAIzKOga','8,4',3,8,4,'2025-05-21 16:33:18'),(64,22,'QWKAIzKOga','9,4',4,9,4,'2025-05-21 16:33:19'),(65,22,'WrEQtzKEqd','9,6',5,9,6,'2025-05-21 16:33:22'),(66,22,'WrEQtzKEqd','6,4',6,6,4,'2025-05-21 16:33:24'),(67,22,'QWKAIzKOga','10,4',7,10,4,'2025-05-21 16:33:27'),(68,22,'QWKAIzKOga','11,4',8,11,4,'2025-05-21 16:33:30'),(69,23,'JlZ4fbzQLX','6,3',1,6,3,'2025-05-21 16:34:33'),(70,23,'JlZ4fbzQLX','7,5',2,7,5,'2025-05-21 16:34:34'),(71,23,'JlZ4fbzQLX','6,4',3,6,4,'2025-05-21 16:34:36'),(72,23,'JlZ4fbzQLX','6,5',4,6,5,'2025-05-21 16:34:36'),(73,23,'JlZ4fbzQLX','6,6',5,6,6,'2025-05-21 16:34:36'),(74,23,'JlZ4fbzQLX','6,7',6,6,7,'2025-05-21 16:34:37'),(75,27,'QWKAIzKOga','6,5',1,6,5,'2025-05-21 16:52:37'),(76,27,'JlZ4fbzQLX','6,4',2,6,4,'2025-05-21 16:52:39'),(77,27,'QWKAIzKOga','7,4',3,7,4,'2025-05-21 16:52:42'),(78,27,'JlZ4fbzQLX','8,3',4,8,3,'2025-05-21 16:52:43'),(79,27,'QWKAIzKOga','7,5',5,7,5,'2025-05-21 16:52:45'),(80,27,'JlZ4fbzQLX','8,6',6,8,6,'2025-05-21 16:52:50'),(81,27,'QWKAIzKOga','7,3',7,7,3,'2025-05-21 16:52:51'),(82,27,'JlZ4fbzQLX','8,2',8,8,2,'2025-05-21 16:52:52'),(83,27,'QWKAIzKOga','7,2',9,7,2,'2025-05-21 16:52:53'),(84,27,'JlZ4fbzQLX','7,1',10,7,1,'2025-05-21 16:52:55'),(85,27,'QWKAIzKOga','7,6',11,7,6,'2025-05-21 16:52:56'),(86,28,'QWKAIzKOga','7,5',1,7,5,'2025-05-21 16:55:21'),(87,28,'JlZ4fbzQLX','8,4',2,8,4,'2025-05-21 16:55:35'),(88,28,'QWKAIzKOga','6,6',3,6,6,'2025-05-21 16:55:37'),(89,28,'JlZ4fbzQLX','8,6',4,8,6,'2025-05-21 16:55:39'),(90,37,'V1HcHSAmil','7,5',1,7,5,'2025-05-23 08:39:08'),(91,37,'xwG8m8BeVL','7,4',2,7,4,'2025-05-23 08:39:11'),(92,37,'V1HcHSAmil','8,4',3,8,4,'2025-05-23 08:39:14'),(93,37,'xwG8m8BeVL','7,3',4,7,3,'2025-05-23 08:39:16'),(94,40,'V1HcHSAmil','8,4',1,8,4,'2025-05-23 08:48:26'),(95,40,'fFfQPgSKdz','9,3',2,9,3,'2025-05-23 08:48:27'),(96,40,'V1HcHSAmil','10,4',3,10,4,'2025-05-23 08:48:28'),(97,40,'fFfQPgSKdz','10,3',4,10,3,'2025-05-23 08:48:29'),(98,40,'V1HcHSAmil','9,4',5,9,4,'2025-05-23 08:48:30'),(99,40,'fFfQPgSKdz','8,3',6,8,3,'2025-05-23 08:48:31'),(100,40,'V1HcHSAmil','7,4',7,7,4,'2025-05-23 08:48:32'),(101,40,'fFfQPgSKdz','7,3',8,7,3,'2025-05-23 08:48:33'),(102,40,'V1HcHSAmil','6,4',9,6,4,'2025-05-23 08:48:34'),(103,42,'V8Oc012oA1','9,6',1,9,6,'2025-05-23 09:05:09'),(104,42,'vdlLAOQ4Op','11,5',2,11,5,'2025-05-23 09:05:19'),(105,42,'V8Oc012oA1','10,6',3,10,6,'2025-05-23 09:05:21'),(106,42,'vdlLAOQ4Op','10,5',4,10,5,'2025-05-23 09:05:22'),(107,42,'V8Oc012oA1','11,6',5,11,6,'2025-05-23 09:05:23'),(108,42,'vdlLAOQ4Op','12,5',6,12,5,'2025-05-23 09:05:24'),(109,42,'V8Oc012oA1','12,6',7,12,6,'2025-05-23 09:05:25'),(110,42,'vdlLAOQ4Op','13,6',8,13,6,'2025-05-23 09:05:26'),(111,42,'V8Oc012oA1','9,7',9,9,7,'2025-05-23 09:05:30'),(112,42,'vdlLAOQ4Op','7,6',10,7,6,'2025-05-23 09:05:31'),(113,42,'V8Oc012oA1','8,6',11,8,6,'2025-05-23 09:05:32'),(114,47,'G3oEf0cceX','9,3',1,9,3,'2025-05-23 09:14:37'),(115,47,'RFL1Naoe34','8,3',2,8,3,'2025-05-23 09:14:38'),(116,47,'G3oEf0cceX','10,4',3,10,4,'2025-05-23 09:14:41'),(117,47,'RFL1Naoe34','8,2',4,8,2,'2025-05-23 09:14:42'),(118,47,'G3oEf0cceX','8,4',5,8,4,'2025-05-23 09:14:43'),(119,47,'RFL1Naoe34','7,2',6,7,2,'2025-05-23 09:14:45'),(120,47,'G3oEf0cceX','5,2',7,5,2,'2025-05-23 09:14:49'),(121,47,'RFL1Naoe34','6,3',8,6,3,'2025-05-23 09:14:52'),(122,47,'G3oEf0cceX','6,2',9,6,2,'2025-05-23 09:15:00'),(123,47,'RFL1Naoe34','8,1',10,8,1,'2025-05-23 09:15:01'),(124,47,'G3oEf0cceX','5,3',11,5,3,'2025-05-23 09:15:02'),(125,47,'RFL1Naoe34','5,4',12,5,4,'2025-05-23 09:15:05'),(126,47,'G3oEf0cceX','5,5',13,5,5,'2025-05-23 09:15:06'),(127,47,'RFL1Naoe34','4,5',14,4,5,'2025-05-23 09:15:07'),(128,48,'G3oEf0cceX','9,3',1,9,3,'2025-05-23 09:24:41'),(129,48,'RFL1Naoe34','10,3',2,10,3,'2025-05-23 09:24:43'),(130,48,'G3oEf0cceX','11,3',3,11,3,'2025-05-23 09:24:44'),(131,48,'RFL1Naoe34','11,4',4,11,4,'2025-05-23 09:24:45'),(132,48,'G3oEf0cceX','10,2',5,10,2,'2025-05-23 09:24:49'),(133,48,'RFL1Naoe34','9,2',6,9,2,'2025-05-23 09:24:50'),(134,48,'G3oEf0cceX','11,1',7,11,1,'2025-05-23 09:24:52'),(135,48,'RFL1Naoe34','8,1',8,8,1,'2025-05-23 09:24:53'),(136,48,'G3oEf0cceX','7,0',9,7,0,'2025-05-23 09:24:55'),(137,48,'RFL1Naoe34','12,5',10,12,5,'2025-05-23 09:24:56'),(138,49,'G3oEf0cceX','7,6',1,7,6,'2025-05-23 09:29:36'),(139,49,'RFL1Naoe34','8,5',2,8,5,'2025-05-23 09:29:37'),(140,49,'G3oEf0cceX','8,7',3,8,7,'2025-05-23 09:29:40'),(141,49,'RFL1Naoe34','9,8',4,9,8,'2025-05-23 09:29:42'),(142,49,'G3oEf0cceX','6,5',5,6,5,'2025-05-23 09:29:44'),(143,49,'RFL1Naoe34','6,4',6,6,4,'2025-05-23 09:29:45'),(144,49,'G3oEf0cceX','5,4',7,5,4,'2025-05-23 09:29:47'),(145,49,'RFL1Naoe34','7,4',8,7,4,'2025-05-23 09:29:48'),(146,49,'G3oEf0cceX','4,3',9,4,3,'2025-05-23 09:29:49'),(147,51,'RFL1Naoe34','7,5',1,7,5,'2025-05-23 09:34:43'),(148,51,'G3oEf0cceX','8,6',2,8,6,'2025-05-23 09:34:44'),(149,51,'RFL1Naoe34','9,5',3,9,5,'2025-05-23 09:34:45'),(150,51,'G3oEf0cceX','8,7',4,8,7,'2025-05-23 09:34:47'),(151,51,'RFL1Naoe34','8,5',5,8,5,'2025-05-23 09:34:48'),(152,51,'G3oEf0cceX','8,8',6,8,8,'2025-05-23 09:34:49'),(153,51,'RFL1Naoe34','10,5',7,10,5,'2025-05-23 09:34:50'),(154,51,'G3oEf0cceX','8,9',8,8,9,'2025-05-23 09:34:53'),(155,51,'RFL1Naoe34','11,5',9,11,5,'2025-05-23 09:34:54'),(156,52,'G3oEf0cceX','14,7',1,14,7,'2025-05-23 09:43:39'),(157,52,'RFL1Naoe34','7,6',2,7,6,'2025-05-23 09:43:42'),(158,52,'G3oEf0cceX','11,7',3,11,7,'2025-05-23 09:43:43'),(159,52,'RFL1Naoe34','8,8',4,8,8,'2025-05-23 09:43:44'),(160,52,'G3oEf0cceX','9,9',5,9,9,'2025-05-23 09:43:49'),(161,52,'RFL1Naoe34','7,7',6,7,7,'2025-05-23 09:43:52'),(162,52,'G3oEf0cceX','12,7',7,12,7,'2025-05-23 09:43:54'),(163,52,'RFL1Naoe34','7,8',8,7,8,'2025-05-23 09:43:55'),(164,52,'G3oEf0cceX','10,7',9,10,7,'2025-05-23 09:43:58'),(165,52,'RFL1Naoe34','7,9',10,7,9,'2025-05-23 09:43:59'),(166,52,'G3oEf0cceX','13,7',11,13,7,'2025-05-23 09:44:01'),(167,53,'G3oEf0cceX','9,8',1,9,8,'2025-05-23 09:51:52'),(168,53,'RFL1Naoe34','7,6',2,7,6,'2025-05-23 09:51:54'),(169,55,'G3oEf0cceX','11,5',1,11,5,'2025-05-23 09:55:52'),(170,55,'RFL1Naoe34','10,4',2,10,4,'2025-05-23 09:55:54'),(171,55,'G3oEf0cceX','10,6',3,10,6,'2025-05-23 09:55:58'),(172,55,'RFL1Naoe34','12,4',4,12,4,'2025-05-23 09:56:02'),(173,55,'G3oEf0cceX','9,7',5,9,7,'2025-05-23 09:56:06'),(174,56,'G3oEf0cceX','3,9',1,3,9,'2025-05-23 10:04:49'),(175,56,'RFL1Naoe34','4,8',2,4,8,'2025-05-23 10:04:53'),(176,56,'G3oEf0cceX','3,8',3,3,8,'2025-05-23 10:04:55'),(177,56,'RFL1Naoe34','3,7',4,3,7,'2025-05-23 10:04:58'),(178,56,'G3oEf0cceX','3,10',5,3,10,'2025-05-23 10:05:00'),(179,56,'RFL1Naoe34','5,9',6,5,9,'2025-05-23 10:05:02'),(180,56,'G3oEf0cceX','3,11',7,3,11,'2025-05-23 10:05:07'),(181,56,'RFL1Naoe34','6,10',8,6,10,'2025-05-23 10:05:08'),(182,56,'G3oEf0cceX','3,12',9,3,12,'2025-05-23 10:05:10'),(183,58,'G3oEf0cceX','8,4',1,8,4,'2025-05-23 10:09:58'),(184,58,'RFL1Naoe34','8,5',2,8,5,'2025-05-23 10:09:59');
/*!40000 ALTER TABLE `move` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `replay_request`
--

DROP TABLE IF EXISTS `replay_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `replay_request` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `game_id` int DEFAULT NULL,
  `player_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`request_id`),
  KEY `game_id` (`game_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `fk_replay_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_replay_player` FOREIGN KEY (`player_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `replay_request`
--

LOCK TABLES `replay_request` WRITE;
/*!40000 ALTER TABLE `replay_request` DISABLE KEYS */;
/*!40000 ALTER TABLE `replay_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skin`
--

DROP TABLE IF EXISTS `skin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skin` (
  `skin_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price` int DEFAULT '0',
  PRIMARY KEY (`skin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skin`
--

LOCK TABLES `skin` WRITE;
/*!40000 ALTER TABLE `skin` DISABLE KEYS */;
/*!40000 ALTER TABLE `skin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_avatar`
--

DROP TABLE IF EXISTS `user_avatar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_avatar` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `avatar_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `avatar_id` (`avatar_id`),
  CONSTRAINT `fk_user_avatar_avatar` FOREIGN KEY (`avatar_id`) REFERENCES `avatar` (`avatar_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_avatar_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_avatar`
--

LOCK TABLES `user_avatar` WRITE;
/*!40000 ALTER TABLE `user_avatar` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_avatar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_skin`
--

DROP TABLE IF EXISTS `user_skin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_skin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `skin_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `skin_id` (`skin_id`),
  CONSTRAINT `fk_user_skin_skin` FOREIGN KEY (`skin_id`) REFERENCES `skin` (`skin_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_skin_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_skin`
--

LOCK TABLES `user_skin` WRITE;
/*!40000 ALTER TABLE `user_skin` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_skin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `displayName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `users_chk_1` CHECK ((char_length(`displayName`) between 3 and 50))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('7cbkmeVKwi','sinh',NULL),('BnDC8QsRDy','Đôn',NULL),('dYRS4kFOF6','Sinh',NULL),('eItlm5OB3J','sinh2307',NULL),('ezBNHaIOS5','Sinh',NULL),('fFfQPgSKdz','Sinh',NULL),('G3oEf0cceX','king',NULL),('hoXRVjYibG','sinh2307',NULL),('iQvDlyRt8q','Sinh',NULL),('IV9Dz4f08o','Sinh',NULL),('JlZ4fbzQLX','sinh',NULL),('JTKJlyZgD6','sinh2307',NULL),('mAPpT4CPbT','Din',NULL),('MSajhWI46m','Sinh',NULL),('NqtK6ESkOT','Đôn',NULL),('QllQ2mn7V4','King',NULL),('QWKAIzKOga','Đôn',NULL),('RFL1Naoe34','Sinh',NULL),('rvoIUFcCVU','King',NULL),('uH2v1nVcql','sinh2307',NULL),('user1','Nguyễn Văn An','/static/images/default_avatar.png'),('user10','Lý Thị Khánh','/static/images/default_avatar.png'),('user11','Hồ Văn Lộc','/static/images/avatar1.png'),('user12','Mai Thị Minh','/static/images/avatar2.png'),('user13','Đỗ Văn Năm','/static/images/default_avatar.png'),('user14','Huỳnh Thị Oanh','/static/images/avatar2.png'),('user15','Phan Văn Phúc','/static/images/avatar1.png'),('user16','Trương Thị Quỳnh','/static/images/default_avatar.png'),('user17','Dương Văn Rồng','/static/images/avatar1.png'),('user18','Võ Thị Sen','/static/images/avatar2.png'),('user19','Đinh Văn Tâm','/static/images/default_avatar.png'),('user2','Trần Thị Bình','/static/images/avatar2.png'),('user20','Nguyễn Thị Uyên','/static/images/avatar2.png'),('user3','Lê Văn Cường','/static/images/avatar1.png'),('user4','Phạm Thị Dung','/static/images/default_avatar.png'),('user5','Hoàng Văn Em','/static/images/avatar1.png'),('user6','Ngô Thị Phương','/static/images/avatar2.png'),('user7','Vũ Văn Giàu','/static/images/default_avatar.png'),('user8','Đặng Thị Hồng','/static/images/avatar2.png'),('user9','Bùi Văn Inox','/static/images/avatar1.png'),('V1HcHSAmil','King',NULL),('V8Oc012oA1','King',NULL),('vdlLAOQ4Op','Hehee',NULL),('w4UOvX1Gka','sinh2307',NULL),('WrEQtzKEqd','sinh',NULL),('xwG8m8BeVL','Sinh',NULL),('Y1ChbRPST0','sinh2307',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-23 17:16:12
