-- MySQL dump 10.13  Distrib 8.0.27, for macos11 (x86_64)
--
-- Host: localhost    Database: course_selection_manage
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `achievement`
--

DROP TABLE IF EXISTS `achievement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achievement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `score` decimal(10,2) DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `year` varchar(32) DEFAULT NULL,
  `semester` varchar(32) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `achievement_ibfk_1` (`course_id`) USING BTREE,
  KEY `achievement_ibfk_2` (`student_id`) USING BTREE,
  CONSTRAINT `achievement_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `achievement_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievement`
--

LOCK TABLES `achievement` WRITE;
/*!40000 ALTER TABLE `achievement` DISABLE KEYS */;
INSERT INTO `achievement` VALUES (1,76.00,2,8,'2023-2024','1','2025-04-25 07:36:03','2025-04-25 07:36:03'),(2,85.00,3,8,'2024-2025','2','2025-04-25 07:36:03','2025-04-25 07:36:03'),(3,85.00,2,9,'2024-2025','3','2025-04-25 07:36:03','2025-04-25 07:36:03'),(11,65.00,4,5,'2023-2024','1','2025-04-25 07:36:03','2025-04-25 07:36:03'),(12,33.00,5,5,'2024-2025','2','2025-04-25 07:36:03','2025-04-25 07:36:03'),(13,56.00,2,11,'2024-2025','3','2025-04-25 07:36:03','2025-04-25 07:36:03'),(14,88.00,2,12,'2024-2025','1','2025-04-25 07:36:03','2025-04-25 07:36:03'),(15,93.00,1,11,'2023-2024','2','2025-04-25 07:36:03','2025-04-25 07:36:03'),(16,45.00,6,1,'2024-2025','3','2025-04-25 07:36:03','2025-04-25 07:36:03'),(17,76.00,4,1,'2024-2025','1','2025-04-25 07:36:03','2025-04-25 07:36:03'),(18,96.00,1,22,'2024-2025','3','2025-04-25 07:36:03','2025-04-25 07:36:03'),(19,59.00,12,29,'2024-2025','1','2025-04-25 07:36:03','2025-04-25 07:36:03'),(20,99.00,13,29,'2024-2025','2','2025-04-25 07:36:03','2025-04-25 07:36:03'),(21,79.00,12,30,'2024-2025','3','2025-04-25 07:36:03','2025-04-25 07:36:03'),(22,59.00,10,15,'2024-2025','1','2025-04-25 07:36:03','2025-04-25 07:36:03'),(23,61.00,12,15,'2024-2025','2','2025-04-25 07:36:03','2025-04-25 07:36:03'),(25,71.50,10,30,'2024-2025','3','2025-04-25 07:36:03','2025-04-25 07:36:03'),(26,60.25,10,5,'2025-2026','1','2025-04-25 07:36:03','2025-04-25 07:36:03'),(27,72.45,14,5,'2025-2026','2','2025-04-25 07:36:03','2025-04-25 07:36:03');
/*!40000 ALTER TABLE `achievement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `email` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `register_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `description` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `avatar` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `user_ibfk_2` (`email`) USING BTREE,
  KEY `user_ibfk_1` (`role_id`) USING BTREE,
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','admin','admin@qq.com',1,'2024-11-08 14:59:33','2024-11-08 14:59:33','我是超级管理员哦，不要乱动我的账号哟~~~~',1,'超级管理员',''),(2,'admin1','12345678','admin1@qq.com',1,'2024-08-21 10:17:42','2024-08-21 10:17:42','嘿嘿嘿1111',1,NULL,NULL),(20,'chaxun','chaxun',NULL,2,'2024-11-08 14:59:33','2024-11-08 14:59:33','查询员',1,'查询员',NULL);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit`
--

DROP TABLE IF EXISTS `audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `op_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `op_ip` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `op_user` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `op_module` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `op_event` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=207 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit`
--

LOCK TABLES `audit` WRITE;
/*!40000 ALTER TABLE `audit` DISABLE KEYS */;
INSERT INTO `audit` VALUES (1,'2024-08-21 17:47:29','127.0.0.1','admin','登录','账号登录'),(2,'2024-08-21 18:00:37','127.0.0.1','admin','登录','账号登录'),(3,'2024-08-21 18:01:15','127.0.0.1','admin','登录','账号退出登录'),(4,'2024-08-21 18:02:00','127.0.0.1','chenrui','用户注册','用户名:chenrui注册，密码:12345678'),(5,'2024-08-21 18:04:26','127.0.0.1','chenrui','重置密码','用户名:chenrui重置密码为d8W2lt1G'),(6,'2024-08-21 18:09:54','127.0.0.1','student','登录','账号登录'),(7,'2024-08-21 18:10:22','127.0.0.1','student','用户中心管理','更新用户信息'),(8,'2024-08-21 18:10:58','127.0.0.1','student','用户中心管理','修改用户密码'),(9,'2024-08-21 18:11:17','127.0.0.1','admin','登录','账号登录'),(10,'2024-08-22 08:31:26','127.0.0.1','admin','教师管理','新增教师信息:wuyue'),(11,'2024-08-22 08:33:27','127.0.0.1','admin','教师管理','更新教师信息:wuyue'),(12,'2024-08-22 08:57:15','127.0.0.1','admin','登录','账号退出登录'),(13,'2024-08-22 09:32:25','127.0.0.1','admin','登录','账号登录'),(14,'2024-08-22 09:32:28','127.0.0.1','admin','登录','账号退出登录'),(15,'2024-08-22 09:35:21','127.0.0.1','admin','登录','账号登录'),(16,'2024-08-22 09:42:54','127.0.0.1','admin','登录','账号退出登录'),(17,'2024-08-22 09:43:05','127.0.0.1','student','登录','账号登录'),(18,'2024-08-22 09:43:19','127.0.0.1','student','选课管理','学生:1 选课:6'),(19,'2024-08-22 09:43:54','127.0.0.1','student','选课管理','取消选课:9'),(20,'2024-08-22 09:44:25','127.0.0.1','student','登录','账号退出登录'),(21,'2024-08-22 09:44:31','127.0.0.1','admin','登录','账号登录'),(22,'2024-08-22 09:44:46','127.0.0.1','admin','登录','账号退出登录'),(23,'2024-08-22 09:44:54','127.0.0.1','student','登录','账号登录'),(24,'2024-08-22 09:45:02','127.0.0.1','student','选课管理','学生:1 选课:4'),(25,'2024-08-22 09:45:07','127.0.0.1','student','登录','账号退出登录'),(26,'2024-08-22 09:45:15','127.0.0.1','admin','登录','账号登录'),(27,'2024-08-22 11:07:37','127.0.0.1','admin','权限管理','更新权限条目:2'),(28,'2024-08-22 11:08:52','127.0.0.1','admin','登录','账号退出登录'),(29,'2024-08-22 11:10:05','127.0.0.1','zhangsan','登录','账号登录'),(30,'2024-08-22 11:10:26','127.0.0.1','zhangsan','登录','账号退出登录'),(31,'2024-08-22 11:10:34','127.0.0.1','zhangsan','登录','账号登录'),(32,'2024-08-22 11:12:13','127.0.0.1','zhangsan','选课管理','新增课程:室内设计'),(33,'2024-08-22 11:12:55','127.0.0.1','zhangsan','登录','账号退出登录'),(34,'2024-08-22 11:13:02','127.0.0.1','admin','登录','账号登录'),(35,'2024-08-22 13:55:53','127.0.0.1','admin','登录','账号退出登录'),(36,'2024-08-22 13:59:03','127.0.0.1','admin','登录','账号登录'),(37,'2024-08-22 14:56:10','127.0.0.1','admin','用户中心','上传了文件: logo.bb6bc725.png'),(38,'2024-08-22 15:46:48','127.0.0.1','admin','用户中心','上传了文件并更新了头像: C.png'),(39,'2024-08-22 15:50:18','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(40,'2024-08-22 15:52:13','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(41,'2024-08-22 15:53:24','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(42,'2024-08-22 15:56:51','127.0.0.1','admin','登录','账号登录'),(43,'2024-08-22 15:57:50','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(44,'2024-08-22 15:59:24','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(45,'2024-08-22 16:02:09','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(46,'2024-08-22 16:03:07','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(47,'2024-08-22 16:04:35','127.0.0.1','admin','登录','账号退出登录'),(48,'2024-08-22 16:04:41','127.0.0.1','admin','登录','账号登录'),(49,'2024-08-22 16:06:16','127.0.0.1','admin','用户中心','上传了文件并更新了头像: htp_admin_v2.png'),(50,'2024-08-22 16:07:00','127.0.0.1','admin','登录','账号退出登录'),(51,'2024-08-22 16:08:05','127.0.0.1','admin','登录','账号登录'),(52,'2024-08-22 16:15:17','127.0.0.1','admin','登录','账号退出登录'),(53,'2024-08-22 16:15:51','127.0.0.1','admin','登录','账号登录'),(54,'2024-08-22 16:33:35','127.0.0.1','admin','登录','账号退出登录'),(55,'2024-08-22 16:33:44','127.0.0.1','zhangsan','登录','账号登录'),(56,'2024-08-22 16:34:08','127.0.0.1','zhangsan','选课管理','新增课程:自由泳学习'),(57,'2024-08-22 16:39:06','127.0.0.1','zhangsan','选课管理','删除课程条目:8'),(58,'2024-08-22 16:39:50','127.0.0.1','zhangsan','登录','账号退出登录'),(59,'2024-08-22 16:39:56','127.0.0.1','zhangsan','登录','账号登录'),(60,'2024-08-22 16:44:27','127.0.0.1','zhangsan','登录','账号退出登录'),(61,'2024-08-22 16:44:33','127.0.0.1','admin','登录','账号登录'),(62,'2024-08-22 17:01:40','127.0.0.1','admin','角色管理','更新角色信息:学生'),(63,'2024-08-22 17:22:57','127.0.0.1','admin','登录','账号退出登录'),(64,'2024-08-22 17:23:05','127.0.0.1','liyifan','登录','账号登录'),(65,'2024-08-22 17:24:52','127.0.0.1','liyifan','选课管理','新增课程:影视名片鉴赏'),(66,'2024-08-22 17:24:54','127.0.0.1','liyifan','登录','账号退出登录'),(67,'2024-08-22 17:25:00','127.0.0.1','admin','登录','账号登录'),(68,'2024-08-22 17:33:15','127.0.0.1','admin','登录','账号登录'),(69,'2024-08-22 17:34:13','127.0.0.1','admin','登录','账号登录'),(70,'2024-08-22 17:40:44','127.0.0.1','admin','登录','账号退出登录'),(71,'2024-08-22 17:40:50','127.0.0.1','admin','登录','账号登录'),(72,'2024-08-22 17:48:44','127.0.0.1','admin','登录','账号退出登录'),(73,'2024-08-22 17:48:50','127.0.0.1','admin','登录','账号登录'),(74,'2024-08-22 17:52:30','127.0.0.1','admin','用户中心管理','更新用户信息'),(75,'2024-08-22 17:55:53','127.0.0.1','admin','用户中心管理','修改用户密码'),(76,'2024-08-22 17:58:18','127.0.0.1','admin','用户中心管理','修改用户密码'),(77,'2024-08-22 17:59:47','127.0.0.1','admin','用户中心管理','修改用户密码'),(78,'2024-08-22 18:04:53','127.0.0.1','admin','登录','账号退出登录'),(79,'2024-08-22 18:05:02','127.0.0.1','admin','登录','账号登录'),(80,'2024-08-22 18:05:16','127.0.0.1','admin','用户中心管理','修改用户密码'),(81,'2024-08-22 18:06:33','127.0.0.1','admin','登录','账号退出登录'),(82,'2024-08-22 18:06:39','127.0.0.1','admin','登录','账号登录'),(83,'2024-08-22 18:06:54','127.0.0.1','admin','用户中心管理','修改用户密码'),(84,'2024-08-22 18:08:32','127.0.0.1','admin','登录','账号登录'),(85,'2024-08-22 18:08:51','127.0.0.1','admin','用户中心管理','修改用户密码'),(86,'2024-08-22 18:13:12','127.0.0.1','admin','登录','账号登录'),(87,'2024-08-22 18:13:29','127.0.0.1','admin','用户中心管理','修改用户密码'),(88,'2024-08-22 18:14:24','127.0.0.1','admin','登录','账号登录'),(89,'2024-08-22 18:14:36','127.0.0.1','admin','用户中心管理','修改用户密码'),(90,'2024-08-23 08:08:42','127.0.0.1','admin','登录','账号登录'),(91,'2024-08-23 08:08:55','127.0.0.1','admin','登录','账号退出登录'),(92,'2024-08-23 08:19:32','127.0.0.1','admin','登录','账号登录'),(93,'2024-08-23 08:23:23','127.0.0.1','admin','登录','账号登录'),(94,'2024-08-23 08:48:05','127.0.0.1','admin','用户中心管理','更新用户信息'),(95,'2024-08-23 09:12:51','127.0.0.1','admin','登录','账号退出登录'),(96,'2024-10-24 15:21:55','127.0.0.1','admin','登录','账号登录'),(97,'2024-10-24 15:38:59','127.0.0.1','admin','登录','账号退出登录'),(98,'2024-10-24 15:39:13','127.0.0.1','zhangsan','登录','账号登录'),(99,'2024-10-24 15:39:26','127.0.0.1','zhangsan','登录','账号退出登录'),(100,'2024-10-24 15:39:35','127.0.0.1','student','登录','账号登录'),(101,'2024-10-24 15:40:07','127.0.0.1','student','登录','账号退出登录'),(102,'2024-10-24 15:40:15','127.0.0.1','admin','登录','账号登录'),(103,'2024-10-28 15:32:26','10.100.10.254','admin','登录','账号登录'),(104,'2024-10-31 15:04:56','127.0.0.1','admin','用户管理','新增账号123456'),(105,'2024-10-31 15:13:36','127.0.0.1','admin','用户管理','删除用户,id: 19'),(106,'2024-10-31 15:14:02','127.0.0.1','admin','用户管理','新增账号123456'),(107,'2024-10-31 15:41:03','127.0.0.1','admin','登录','账号登录'),(108,'2024-10-31 16:08:10','127.0.0.1','admin','用户管理','更新用户信息'),(109,'2024-10-31 16:18:22','127.0.0.1','admin','用户管理','更新用户信息'),(110,'2024-10-31 16:19:07','127.0.0.1','admin','用户管理','更新用户信息'),(111,'2024-10-31 16:21:47','127.0.0.1','admin','用户管理','更新用户信息'),(112,'2024-10-31 16:27:23','127.0.0.1','admin','用户管理','更新用户信息'),(113,'2024-10-31 16:27:32','127.0.0.1','admin','用户管理','更新用户信息'),(114,'2024-10-31 18:32:42','127.0.0.1','admin','用户管理','批量新增账号'),(115,'2024-10-31 19:21:36','127.0.0.1','admin','用户管理','批量新增账号'),(116,'2024-10-31 19:25:24','127.0.0.1','admin','用户管理','批量新增账号'),(117,'2024-10-31 19:26:00','127.0.0.1','admin','用户管理','批量新增账号'),(118,'2024-10-31 23:04:37','127.0.0.1','admin','教师管理','更新教师信息:zhangsan'),(119,'2024-10-31 23:13:31','127.0.0.1','admin','教师管理','新增教师信息:huge'),(120,'2024-10-31 23:44:15','127.0.0.1','admin','教师管理','批量新增教师'),(121,'2024-10-31 23:55:50','127.0.0.1','admin','教师管理','删除教师信息:18'),(122,'2024-11-01 16:03:15','127.0.0.1','admin','选课管理','新增课程:计算机理论'),(123,'2024-11-01 16:22:54','127.0.0.1','admin','选课管理','更新课程:计算机理论'),(124,'2024-11-01 16:24:21','127.0.0.1','admin','选课管理','新增课程:数据结构'),(125,'2024-11-01 16:25:05','127.0.0.1','admin','选课管理','删除课程条目:11'),(126,'2024-11-01 16:48:39','127.0.0.1','admin','课程管理','批量新增课程'),(127,'2024-11-05 17:10:08','127.0.0.1','admin','选课管理','更新成绩: {\'course_name\': \'ps基础\', \'student_name\': \'侯亮平\', \'gradelevel_name\': \'A\'}'),(128,'2024-11-05 17:19:53','127.0.0.1','admin','成绩管理','更新成绩: {\'course_name\': \'ps基础\', \'student_name\': \'侯亮平\', \'score\': 96, \'gradelevel_name\': \'A\'}'),(129,'2024-11-05 17:20:49','127.0.0.1','admin','成绩管理','添加成绩: {\'course_name\': \'数据库\', \'student_name\': \'小鱼儿\', \'score\': 59, \'gradelevel_name\': \'C\'}'),(130,'2024-11-05 17:23:50','127.0.0.1','admin','成绩管理','更新成绩: {\'course_name\': \'插花艺术\', \'student_name\': \'李刚\', \'score\': 77, \'gradelevel_name\': \'B\'}'),(131,'2024-11-05 17:24:08','127.0.0.1','admin','成绩管理','更新成绩: {\'course_name\': \'中国语言文学\', \'student_name\': \'陈凡\', \'score\': 64, \'gradelevel_name\': \'B\'}'),(132,'2024-11-05 17:27:05','127.0.0.1','admin','选课管理','更新课程:影视名片鉴赏'),(133,'2024-11-05 17:27:21','127.0.0.1','admin','选课管理','更新课程:数据库'),(134,'2024-11-05 17:28:29','127.0.0.1','admin','教师管理','更新教师信息:lisi'),(135,'2024-11-05 18:11:08','127.0.0.1','admin','成绩管理','批量新增成绩'),(136,'2024-11-06 15:40:56','127.0.0.1','admin','成绩管理','更新成绩: 中国语言文学-陈凡-65'),(137,'2024-11-06 15:42:04','127.0.0.1','admin','成绩管理','更新成绩: 国学智慧-陈凡-33'),(138,'2024-11-06 16:00:06','127.0.0.1','admin','成绩管理','更新成绩: 插花艺术-王胡-88'),(139,'2024-11-06 16:15:10','127.0.0.1','admin','成绩管理','更新成绩分级信息: B'),(140,'2024-11-06 16:17:16','127.0.0.1','admin','成绩管理','删除成绩分级:3'),(141,'2024-11-06 16:17:34','127.0.0.1','admin','成绩管理','更新成绩分级信息: C'),(142,'2024-11-07 15:28:52','127.0.0.1','admin','成绩管理','添加成绩: 数据库-陈胜-61'),(143,'2024-11-07 15:41:38','127.0.0.1','admin','登录','账号登录'),(144,'2024-11-07 16:10:18','127.0.0.1','admin','成绩管理','更新成绩: 插花艺术-李刚-76'),(145,'2024-11-07 16:11:01','127.0.0.1','admin','成绩管理','添加成绩: 计算机理论-花无缺-72'),(146,'2024-11-07 16:12:26','127.0.0.1','admin','成绩管理','删除成绩条目:24'),(147,'2024-11-07 16:12:42','127.0.0.1','admin','成绩管理','添加成绩: 计算机理论-花无缺-72'),(148,'2024-11-07 16:13:32','127.0.0.1','admin','成绩管理','更新成绩: 计算机理论-花无缺-71'),(149,'2024-11-07 16:13:54','127.0.0.1','admin','成绩管理','添加成绩: 计算机理论-陈凡-60'),(150,'2024-11-07 17:17:31','127.0.0.1','admin','登录','账号登录'),(151,'2024-11-07 21:55:07','127.0.0.1','admin','登录','账号退出登录'),(152,'2024-11-07 21:55:14','127.0.0.1','admin','登录','账号登录'),(153,'2024-11-08 10:46:04','127.0.0.1','admin','登录','账号退出登录'),(154,'2024-11-08 10:46:20','127.0.0.1','zhangsan','登录','账号登录'),(155,'2024-11-08 12:08:21','127.0.0.1','zhangsan','登录','账号退出登录'),(156,'2024-11-08 12:08:35','127.0.0.1','chaxun','登录','账号登录'),(157,'2024-11-08 12:08:44','127.0.0.1','chaxun','登录','账号退出登录'),(158,'2024-11-08 12:08:59','127.0.0.1','chaxun','登录','账号登录'),(159,'2024-11-08 12:15:50','127.0.0.1','chaxun','登录','账号退出登录'),(160,'2024-11-08 12:16:03','127.0.0.1','chaxun','登录','账号登录'),(161,'2024-11-08 14:23:15','127.0.0.1','chaxun','登录','账号退出登录'),(162,'2024-11-08 14:26:59','127.0.0.1','chaxun','登录','账号登录'),(163,'2024-11-08 14:43:24','127.0.0.1','chaxun','登录','账号退出登录'),(164,'2024-11-08 14:43:31','127.0.0.1','admin','登录','账号登录'),(165,'2024-11-08 14:53:58','127.0.0.1','admin','用户中心管理','修改用户密码'),(166,'2024-11-08 14:54:45','127.0.0.1','admin','登录','账号登录'),(167,'2024-11-08 14:54:57','127.0.0.1','admin','用户中心管理','修改用户密码'),(168,'2024-11-08 14:57:11','127.0.0.1','admin','登录','账号登录'),(169,'2024-11-08 14:57:31','127.0.0.1','admin','教师管理','更新教师信息: zhangsan'),(170,'2024-11-08 14:57:37','127.0.0.1','admin','教师管理','更新教师信息: zhangsan'),(171,'2024-11-08 14:57:50','127.0.0.1','admin','用户中心管理','修改用户密码'),(172,'2024-11-08 14:58:31','127.0.0.1','admin','登录','账号登录'),(173,'2024-11-08 14:58:35','127.0.0.1','admin','登录','账号退出登录'),(174,'2024-11-08 14:58:42','127.0.0.1','chaxun','登录','账号登录'),(175,'2024-11-08 14:59:10','127.0.0.1','chaxun','用户中心管理','修改用户密码'),(176,'2024-11-08 14:59:20','127.0.0.1','chaxun','登录','账号登录'),(177,'2024-11-08 14:59:42','127.0.0.1','chaxun','登录','账号退出登录'),(178,'2024-11-08 15:00:14','127.0.0.1','admin','登录','账号登录'),(179,'2024-11-08 15:07:22','127.0.0.1','admin','教师管理','更新教师信息: 8888'),(180,'2024-11-08 15:08:23','127.0.0.1','admin','教师管理','新增教师信息: 9999'),(181,'2024-11-08 16:18:22','127.0.0.1','admin','登录','账号退出登录'),(182,'2024-11-08 16:19:05','127.0.0.1','admin','登录','账号登录'),(183,'2024-11-11 15:51:55','127.0.0.1','admin','登录','账号退出登录'),(184,'2025-04-15 15:07:08','127.0.0.1','admin','选课管理','新增课程: 嵌入式'),(185,'2025-04-15 15:07:55','127.0.0.1','admin','成绩管理','添加成绩: 嵌入式-陈凡-72.45'),(186,'2025-04-15 15:08:49','127.0.0.1','admin','成绩管理','更新成绩: 计算机理论-陈凡-60'),(187,'2025-04-15 15:15:26','127.0.0.1','admin','成绩管理','更新成绩: 计算机理论-陈凡-60.25'),(188,'2025-04-15 15:18:05','127.0.0.1','admin','成绩管理','更新成绩: 计算机理论-花无缺-71.5'),(189,'2025-04-16 14:33:49','127.0.0.1','admin','选课管理','新增课程: 经济学概论'),(190,'2025-04-16 14:34:16','127.0.0.1','admin','选课管理','删除课程条目:15'),(191,'2025-04-16 14:39:52','127.0.0.1','admin','课程管理','批量新增课程'),(192,'2025-04-21 16:07:49','127.0.0.1','admin','教师管理','新增教师信息: '),(193,'2025-04-21 16:15:06','127.0.0.1','admin','教师管理','更新教师信息: '),(194,'2025-04-21 16:18:41','127.0.0.1','admin','教师管理','更新教师信息: '),(195,'2025-04-21 16:30:19','127.0.0.1','admin','用户管理','新增账号: 20250421'),(196,'2025-04-23 15:09:27','127.0.0.1','admin','登录','账号登录'),(197,'2025-04-24 15:40:56','127.0.0.1','admin','用户管理','新增账号: 20250424'),(198,'2025-04-24 15:50:53','127.0.0.1','admin','用户管理','更新用户信息: 20250424'),(199,'2025-04-24 15:51:02','127.0.0.1','admin','用户管理','新增账号: 20250424'),(200,'2025-04-24 16:01:57','127.0.0.1','admin','用户管理','更新用户信息: 20250424'),(201,'2025-04-24 16:02:34','127.0.0.1','admin','用户管理','删除用户,id: [34]'),(202,'2025-04-24 17:05:08','127.0.0.1','admin','课程管理','新增课程: 教会历史2'),(203,'2025-04-24 17:05:40','127.0.0.1','admin','课程管理','更新课程: 教会历史2'),(204,'2025-04-24 17:08:05','127.0.0.1','admin','课程管理','更新课程: 教会历史2'),(205,'2025-04-24 17:09:31','127.0.0.1','admin','课程管理','删除课程条目: [28]'),(206,'2025-04-25 15:42:13','127.0.0.1','admin','教师管理','更新教师信息: id=23');
/*!40000 ALTER TABLE `audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `teaching_time` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `teaching_place` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `allow_stu_num` int DEFAULT NULL,
  `selected_stu_num` int DEFAULT '0',
  `credits` int DEFAULT NULL,
  `startdate` varchar(128) DEFAULT NULL,
  `enddate` varchar(128) DEFAULT NULL,
  `teacher_name` varchar(128) DEFAULT NULL,
  `category` varchar(32) DEFAULT NULL,
  `major_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `course_major_fk` (`major_id`),
  CONSTRAINT `course_major_fk` FOREIGN KEY (`major_id`) REFERENCES `major` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'旧约概论','每周三晚上8:00','逸夫楼6201',30,2,1,'2023-11-01','2024-11-01','张三','圣经研究',1,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(2,'新约概论','每周一、周三晚上8:10','德育楼1207',25,3,2,'2023-11-02','2024-11-01','李思思','圣经研究',1,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(3,'系统神学I','每周二 、周四晚上8:10','德育楼1302',20,2,3,'2023-11-03','2024-11-01','王珊','系统神学',1,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(4,'教会历史I','每周2晚上8:00','信工楼2305',22,2,4,'2023-11-04','2024-11-01','陈伟','历史神学',1,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(5,'讲道学入门','每周2晚上9:00','信工楼2302',28,1,3,'2023-11-05','2024-11-01','李一樊','实践神学',1,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(6,'圣经释经学','每周一晚上8:00','艺术楼1406',15,1,2,'2023-11-06','2024-11-01','胡歌','圣经研究',1,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(7,'圣经希伯来文I','每周五晚上7:30','致远楼3206',10,0,1,'2023-11-07','2024-11-01','黄磊','圣经研究',2,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(9,'圣经希腊文I','每周1晚上8:00','多媒体教学楼1205',30,0,2,'2023-11-08','2024-11-01','宋丹丹','圣经研究',2,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(10,'系统神学进阶','周三','逸夫楼',30,0,3,'2023-10-17','2023-11-16','欧阳锋','系统神学',2,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(12,'讲道学进阶','周四','计算机楼',NULL,0,3,'2024-01-01','2024-05-01','黄磊','实践神学',2,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(13,'教牧辅导与关怀','周一','软件楼',NULL,0,4,'2024-02-01','2024-06-01','宋丹丹','实践神学',2,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(14,'教会管理与领导','','',NULL,0,3,'2025-04-15','2025-04-30','胡歌','实践神学',2,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(16,'改革宗神学专题','','',NULL,0,2,'2024-01-01','2024-05-01','黄磊','系统神学',3,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(17,'神学与文化','','',NULL,0,4,'2024-02-01','2024-06-01','宋丹丹','应用神学',3,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(18,'基督教伦理学',NULL,NULL,NULL,0,1,NULL,NULL,NULL,'伦理学',3,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(19,'当代神学思潮',NULL,NULL,NULL,0,2,NULL,NULL,NULL,'历史神学',3,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(20,'高等系统神学研读',NULL,NULL,NULL,0,3,NULL,NULL,NULL,'系统神学',4,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(21,'教父神学专题',NULL,NULL,NULL,0,4,NULL,NULL,NULL,'历史神学',4,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(22,'神学研究方法论',NULL,NULL,NULL,0,1,NULL,NULL,NULL,'研究方法',4,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(23,'博士论文写作',NULL,NULL,NULL,0,2,NULL,NULL,NULL,'研究方法',4,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(24,'教会增长与更新',NULL,NULL,NULL,0,3,NULL,NULL,NULL,'实践神学',5,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(25,'属灵领导力实践',NULL,NULL,NULL,0,4,NULL,NULL,NULL,'实践神学',5,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(26,'门训与代际传承',NULL,NULL,NULL,0,1,NULL,NULL,NULL,'实践神学',5,'2025-04-25 07:37:53','2025-04-25 07:37:53'),(27,'事工项目设计',NULL,NULL,NULL,0,2,NULL,NULL,NULL,'实地项目',5,'2025-04-25 07:37:53','2025-04-25 07:37:53');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gradelevel`
--

DROP TABLE IF EXISTS `gradelevel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gradelevel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `number` varchar(128) DEFAULT NULL,
  `name` varchar(128) NOT NULL,
  `min_score` decimal(10,2) DEFAULT NULL,
  `max_score` decimal(10,2) DEFAULT NULL,
  `gpa` decimal(4,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `table_name_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gradelevel`
--

LOCK TABLES `gradelevel` WRITE;
/*!40000 ALTER TABLE `gradelevel` DISABLE KEYS */;
INSERT INTO `gradelevel` VALUES (1,'1','A',80.00,100.00,4.00,'2025-04-25 07:38:03','2025-04-25 07:38:03'),(2,'2','B',60.00,79.99,3.00,'2025-04-25 07:38:03','2025-04-25 07:38:03'),(4,'3','C',40.00,59.99,2.00,'2025-04-25 07:38:03','2025-04-25 07:38:03'),(5,'4','D',0.00,39.99,0.00,'2025-04-25 07:38:03','2025-04-25 07:38:03');
/*!40000 ALTER TABLE `gradelevel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `major`
--

DROP TABLE IF EXISTS `major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `major` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `level` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `major_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `major`
--

LOCK TABLES `major` WRITE;
/*!40000 ALTER TABLE `major` DISABLE KEYS */;
INSERT INTO `major` VALUES (1,'神学本科','本科','2025-04-25 07:37:46','2025-04-25 07:37:46'),(2,'道学硕士','硕士','2025-04-25 07:37:46','2025-04-25 07:37:46'),(3,'神学硕士','硕士','2025-04-25 07:37:46','2025-04-25 07:37:46'),(4,'神学博士','博士','2025-04-25 07:37:46','2025-04-25 07:37:46'),(5,'事工博士','博士','2025-04-25 07:37:46','2025-04-25 07:37:46');
/*!40000 ALTER TABLE `major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notice`
--

DROP TABLE IF EXISTS `notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notice` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `content` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `release_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notice`
--

LOCK TABLES `notice` WRITE;
/*!40000 ALTER TABLE `notice` DISABLE KEYS */;
INSERT INTO `notice` VALUES (1,'欢迎使用本管理系统','各位用户：\n    欢迎大家使用本管理系统，使用过程中有任何问题，欢迎联系系统管理员：158XXXXXXXX','2024-08-19 09:56:02'),(2,'系统升级公告','各位用户：\n    本系统将于2024-8-19晚上23：00-24：00点进行系统升级，大升级期间系统不可用，请知晓！','2024-08-19 10:23:44'),(3,'系统使用须知','如有疑问请联系管理员','2024-08-19 12:50:10');
/*!40000 ALTER TABLE `notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `permission_ids` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `description` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'管理员','1,2,3,4,6,7,8,9,10','我就是管理员，好好好'),(2,'教师','2,4','这是普通用户角色'),(3,'学生','2,5','学生角色只能选课和查看成绩哈');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_major`
--

DROP TABLE IF EXISTS `student_major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_major` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `major_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_major__major_fk` (`major_id`),
  KEY `student_major__user_fk` (`student_id`),
  CONSTRAINT `student_major__major_fk` FOREIGN KEY (`major_id`) REFERENCES `major` (`id`),
  CONSTRAINT `student_major__user_fk` FOREIGN KEY (`student_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_major`
--

LOCK TABLES `student_major` WRITE;
/*!40000 ALTER TABLE `student_major` DISABLE KEYS */;
INSERT INTO `student_major` VALUES (1,1,1),(2,2,1),(3,5,1),(4,7,1),(5,8,2),(6,9,2),(7,10,2),(8,11,2),(9,12,3),(10,13,3),(11,14,3),(12,15,3),(13,20,4),(14,22,4),(15,29,4),(16,30,5),(17,31,5),(18,1,2),(19,1,3),(20,2,2);
/*!40000 ALTER TABLE `student_major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `sex` tinyint(1) DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `email` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `rank` varchar(128) DEFAULT NULL,
  `description` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `avatar` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `number` varchar(128) DEFAULT NULL,
  `education` varchar(128) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `teacher_number_uindex` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (1,'zhangsan','张三','12345678',1,'15825465982','zhangsan@qq.com','教授','我是教师1号',NULL,'111112','博士','2025-04-25 07:37:01','2025-04-25 07:37:01'),(14,'lisi','李思思','12345678',0,'15828556459','lisi@qq.com','讲师','22222222222222',NULL,'22222','本科','2025-04-25 07:37:01','2025-04-25 07:37:01'),(15,'wangshan','王珊','11112222',0,'13564585956','wangshan@163.com','副教授','高级教师',NULL,'5555','研究生','2025-04-25 07:37:01','2025-04-25 07:37:01'),(16,'chenwei','陈伟','12345678',1,'13526589569','chenwei@qq.com','教授','高级教师，中共党员，校骨干教师，近几年分别取得市“教坛新秀”、“教学能手”称号，刚聘为校教研员。',NULL,'3542','博士','2025-04-25 07:37:01','2025-04-25 07:37:01'),(17,'liyifan','李一樊','11223344',1,'15854658957','liyifan@qq.com','讲师','多次获市级教学成绩奖;连续两届被评为“教学能手”、“先进教育工作者”;多次执教市区级公开课和示范课。',NULL,'86452','本科','2025-04-25 07:37:01','2025-04-25 07:37:01'),(19,'huge','胡歌','huge',1,'13066669876','13066669876@qq.com','教授','',NULL,'33333','研究生','2025-04-25 07:37:01','2025-04-25 07:37:01'),(20,'huanglei','黄磊','huanglei',1,'19187658888','huanglei@qq.com','教授','',NULL,'7777','博士','2025-04-25 07:37:01','2025-04-25 07:37:01'),(21,'songdandan','宋丹丹','songdandan',0,'18377773456','songdandan@163.com','副教授','',NULL,'8888','本科','2025-04-25 07:37:01','2025-04-25 07:37:01'),(22,'9999','欧阳锋','9999',1,'13649585621','ouyangfeng@qq.com','教授','',NULL,'9999','研究生','2025-04-25 07:37:01','2025-04-25 07:37:01'),(23,'','黄渤','',1,'13066665555','','','',NULL,'','','2025-04-25 07:37:01','2025-04-25 07:42:13');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `email` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `register_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `description` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  `avatar` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `sex` tinyint NOT NULL,
  `hometown` varchar(256) DEFAULT NULL,
  `enrollment_date` varchar(128) DEFAULT NULL,
  `student_type` varchar(32) DEFAULT NULL,
  `fellowship` varchar(128) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `user_username_uindex` (`username`),
  KEY `user_ibfk_1` (`role_id`) USING BTREE,
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'20240101','李龙','12345678','lilong@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44','我是一个学生哈',1,NULL,1,'广州','2024-10-30','1','团契一','13111112222','2025-04-25 07:36:40','2025-04-25 07:36:40'),(2,'20240102','张一','12345678','user111111@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44','嘿嘿嘿1111',1,NULL,1,'惠州','2024-10-29','2','团契一','18322225555','2025-04-25 07:36:40','2025-04-25 07:36:40'),(5,'20240103','陈凡','test2','test2@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44','33333333333',1,NULL,0,'佛山','2024-10-14','3','团契一','13355559999','2025-04-25 07:36:40','2025-04-25 07:36:40'),(7,'20240506','吴用','123456','test1@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44','11111111111111',0,NULL,1,'佛山','2024-10-27','1','团契一','15644443333','2025-04-25 07:36:40','2025-04-25 07:36:40'),(8,'20040603','李刚','12345678','aa@tongtech.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44',NULL,1,NULL,1,'珠海','2024-10-15','2','团契一','18133336666','2025-04-25 07:36:40','2025-04-25 07:36:40'),(9,'20230501','陈烨','adfasdfasdfafd','bb@163.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44',NULL,1,NULL,1,'肇庆','2024-10-23','3','团契二','19155557777','2025-04-25 07:36:40','2025-04-25 07:36:40'),(10,'20210406','殷撤','cccccccc','cc@163.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44','22223234adfasdf',1,NULL,0,'清远','2024-10-14','1','团契3','13355554444','2025-04-25 07:36:40','2025-04-25 07:36:40'),(11,'20200509','胡美','ddddd','dddd@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44',NULL,0,NULL,0,'江门','2024-10-04','2','团契3','12266669999','2025-04-25 07:36:40','2025-04-25 07:36:40'),(12,'20190801','王胡','asdfasdfasdfasdf','aasdfasdf@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44','adsafasdfasdfasdfa',1,NULL,1,'深圳','2024-10-05','1','团契3','15566667777','2025-04-25 07:36:40','2025-04-25 07:36:40'),(13,'20241203','张三丰','adsadsfadsfadfadfa','adsfafa@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44','25454545787822',0,NULL,1,'广州','2024-10-12','2','团契3','18899995555','2025-04-25 07:36:40','2025-04-25 07:36:40'),(14,'20240708','贾秀秀','rrrrr','rrrrr@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44',NULL,1,NULL,0,'香港','2024-10-26','1','团契二','13266664444','2025-04-25 07:36:40','2025-04-25 07:36:40'),(15,'20180516','陈胜','asdfasdfadfasdf','1234444@qq.com',3,'2024-11-04 14:27:44','2024-11-04 14:27:44',NULL,1,NULL,1,'澳门','2024-10-17','2','团契二','15644449999','2025-04-25 07:36:40','2025-04-25 07:36:40'),(20,'20240109','吴广','d8W2lt1G','chenrui@qq.com',3,'2025-04-23 15:04:55','2025-04-23 15:04:55',NULL,1,NULL,0,'汕头','2024-10-21','1','团契3','13155552222','2025-04-25 07:36:40','2025-04-25 07:36:40'),(22,'123456','侯亮平','123456','5544982@qq.com',3,'2024-10-31 15:14:02',NULL,'',1,NULL,1,'湖南','2024-09-01','类别一','团契 10','13066665555','2025-04-25 07:36:40','2025-04-25 07:36:40'),(29,'156894','李四','156894','xiaoyuuer@qq.com',3,'2025-04-23 15:04:55','2025-04-23 15:04:55','',1,NULL,0,'河北','2024-01-01','类别1','团契一','15066887744','2025-04-25 07:36:40','2025-04-25 07:36:40'),(30,'124956','王五','124956','huawuque@qq.com',3,'2025-04-23 15:04:55','2025-04-23 15:04:55','',1,NULL,1,'河南','2024-05-06','类别9','团契四','19155223344','2025-04-25 07:36:40','2025-04-25 07:36:40'),(31,'20250421','张伟','20250421','',3,'2025-04-23 15:04:55','2025-04-23 15:04:55','',1,NULL,1,'','','','','','2025-04-25 07:36:40','2025-04-25 07:36:40');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-25 16:52:46
