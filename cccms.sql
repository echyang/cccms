-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: cccms_2
-- ------------------------------------------------------
-- Server version	5.5.38-0+wheezy1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `article_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article`
--

LOCK TABLES `article` WRITE;
/*!40000 ALTER TABLE `article` DISABLE KEYS */;
/*!40000 ALTER TABLE `article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lft` int(11) DEFAULT NULL,
  `rgt` int(11) DEFAULT NULL,
  `layer` int(11) DEFAULT NULL,
  `data_model_id` int(11) DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_category_title` (`title`),
  KEY `data_model_id` (`data_model_id`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`data_model_id`) REFERENCES `data_model` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,1,2,0,1,'ROOT','','','','','2014-07-29 22:55:47','2014-07-29 22:55:47'),(2,2,3,1,4,'关于我们','滨州,基督,协会','','','','2014-07-29 13:04:51','2014-09-25 08:35:03'),(3,4,11,1,1,'新闻中心','','','','','2014-07-29 13:05:13','2014-09-25 08:32:45'),(4,5,8,2,1,'企业动态','','','','','2014-07-29 13:05:34','2014-07-29 13:05:34'),(5,9,10,2,1,'行业新闻','','','','','2014-07-29 13:07:22','2014-07-29 13:07:22'),(6,12,17,1,2,'产品展示','','','','','2014-07-29 13:07:42','2014-09-25 08:35:11'),(7,13,14,2,2,'产品分类A','','','','','2014-07-29 13:07:59','2014-09-25 08:35:17'),(8,15,16,2,2,'产品分类B','','','','','2014-07-29 13:08:15','2014-09-25 08:35:25'),(9,18,19,1,1,'在线留言','','','','','2014-07-29 13:08:38','2014-07-29 13:08:38'),(10,20,21,1,4,'联系方式','','','','','2014-07-29 13:08:54','2014-09-25 08:35:32'),(11,6,7,3,1,'企业动态01','','','','','2014-07-30 04:58:20','2014-09-25 08:32:50');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `config`
--

DROP TABLE IF EXISTS `config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `sitename` varchar(64) DEFAULT NULL,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `domain` varchar(100) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `company_site` varchar(100) DEFAULT NULL,
  `linkman` varchar(100) DEFAULT NULL,
  `tel` varchar(100) DEFAULT NULL,
  `icp` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_config_sitename` (`sitename`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config`
--

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;
INSERT INTO `config` VALUES (1,'2014-07-29 12:23:29','2014-07-29 12:24:01','滨州基督教协会','滨州,基督,协会','滨州基督教协会','www.bzchruch.com','滨州基督教协会','','王国强','18454350968','鲁ICP备10086号');
/*!40000 ALTER TABLE `config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_model`
--

DROP TABLE IF EXISTS `data_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `code` varchar(64) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_data_model_name` (`name`),
  UNIQUE KEY `ix_data_model_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_model`
--

LOCK TABLES `data_model` WRITE;
/*!40000 ALTER TABLE `data_model` DISABLE KEYS */;
INSERT INTO `data_model` VALUES (1,'文章','article','',0,'2014-07-29 12:14:09','2014-07-29 12:14:09'),(2,'产品','product','',0,'2014-07-29 12:14:24','2014-07-29 12:14:24'),(3,'图库','picture','',0,'2014-07-29 12:15:42','2014-07-29 12:15:42'),(4,'单页','single_page','',0,'2014-07-29 12:16:06','2014-07-29 12:16:06');
/*!40000 ALTER TABLE `data_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_group_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group`
--

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;
INSERT INTO `group` VALUES (1,'2014-02-21 14:19:14','2014-02-24 15:13:26','test','test'),(2,'2014-02-21 14:19:22','2014-02-24 15:14:03','user','user001'),(3,'2014-02-21 14:19:29','2014-02-21 14:19:29','admin','admin'),(4,'2014-02-21 14:19:45','2014-02-21 14:19:45','superadmin','superadmin'),(5,'2014-03-20 13:18:59','2014-03-20 13:18:59','系统管理员','系统管理员'),(6,'2014-03-24 23:12:26','2014-03-24 23:12:26','普通用户',''),(7,'2014-04-23 15:59:43','2014-04-23 15:59:43','test55','');
/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `member_group_id` int(11) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_member_email` (`email`),
  UNIQUE KEY `ix_member_username` (`username`),
  KEY `member_group_id` (`member_group_id`),
  CONSTRAINT `member_ibfk_1` FOREIGN KEY (`member_group_id`) REFERENCES `member_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,1,'test','test999@163.com','test999',1,'2014-07-30 04:33:23','2014-07-30 04:33:23'),(2,1,'test001','test001@cccms.org','test001',1,'2014-07-30 04:33:58','2014-07-30 04:33:58');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_group`
--

DROP TABLE IF EXISTS `member_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_member_group_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_group`
--

LOCK TABLES `member_group` WRITE;
/*!40000 ALTER TABLE `member_group` DISABLE KEYS */;
INSERT INTO `member_group` VALUES (1,'默认会员组','','2014-07-29 23:10:55','2014-07-29 23:10:55'),(2,'VIP会员','','2014-07-30 04:34:27','2014-07-30 04:34:27');
/*!40000 ALTER TABLE `member_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migrate_version`
--

DROP TABLE IF EXISTS `migrate_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `migrate_version` (
  `repository_id` varchar(250) NOT NULL,
  `repository_path` text,
  `version` int(11) DEFAULT NULL,
  PRIMARY KEY (`repository_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migrate_version`
--

LOCK TABLES `migrate_version` WRITE;
/*!40000 ALTER TABLE `migrate_version` DISABLE KEYS */;
INSERT INTO `migrate_version` VALUES ('database repository','/root/code/cccms/project/db_repostitory',0);
/*!40000 ALTER TABLE `migrate_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `picture`
--

DROP TABLE IF EXISTS `picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `picture_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `picture_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picture`
--

LOCK TABLES `picture` WRITE;
/*!40000 ALTER TABLE `picture` DISABLE KEYS */;
/*!40000 ALTER TABLE `picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_picture`
--

DROP TABLE IF EXISTS `product_picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_picture_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `product_picture_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_picture`
--

LOCK TABLES `product_picture` WRITE;
/*!40000 ALTER TABLE `product_picture` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_username` (`username`),
  UNIQUE KEY `ix_user_email` (`email`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'2014-02-21 14:22:40','2014-02-24 15:51:04',2,'user001','user001@test.com','user0001',0),(2,'2014-02-21 14:23:00','2014-09-27 08:19:21',3,'admin','admin@admin8.com','admin888',1),(3,'2014-02-21 14:23:20','2014-02-21 14:23:20',4,'root','root@admin.com','test992',1),(4,'2014-02-22 14:06:44','2014-02-22 14:06:44',1,'test555','test555@test.com','test555',1),(5,'2014-02-22 14:07:14','2014-03-26 14:18:05',1,'test666','test666@test.com','test666',1),(6,'2014-02-22 14:07:29','2014-02-22 14:07:29',1,'test6665','test7@test.com','tst555543',1),(7,'2014-02-24 15:44:33','2014-02-24 15:44:33',1,'test','test','test',1),(9,'2014-02-24 15:45:10','2014-02-24 15:45:10',1,'test55565','test55555@test.com','test3323',1),(10,'2014-02-24 15:45:28','2014-02-24 15:45:28',1,'test001','test001@test.com','test888',1),(11,'2014-02-24 15:45:49','2014-02-24 15:45:49',1,'test002','test001@test.com.cn','test',1),(12,'2014-02-24 15:46:09','2014-02-24 15:46:09',1,'test556','test123@test.com','test099',1),(13,'2014-02-24 15:51:32','2014-02-24 15:51:32',1,'test222111','testst@test002.com','test555',1),(15,'2014-03-25 22:29:39','2014-03-25 22:29:39',1,'ttetsest001','test@test0071.com','tets',1),(16,'2014-03-25 22:30:10','2014-03-25 22:38:51',1,'admin007','admin007@test.com','test222',1),(17,'2014-03-28 23:40:08','2014-03-28 23:40:08',1,'admin221','admin@admin.com','admin',1),(18,'2014-03-28 23:40:42','2014-03-29 13:59:42',1,'root123','root123@admin.com','root123',1),(19,'2014-03-31 16:22:03','2014-03-31 16:22:03',1,'test5555','test5542','test',1);
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

-- Dump completed on 2014-09-27 16:20:47
