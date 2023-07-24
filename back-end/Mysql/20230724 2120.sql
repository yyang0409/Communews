CREATE DATABASE  IF NOT EXISTS `communews` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `communews`;
-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: communews
-- ------------------------------------------------------
-- Server version	5.7.36-log

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
-- Table structure for table `tb_collection_record`
--

DROP TABLE IF EXISTS `tb_collection_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_collection_record` (
  `id_collection_record` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_keyword` int(11) NOT NULL,
  `islike` char(1) CHARACTER SET latin1 NOT NULL,
  `rating` int(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id_collection_record`),
  KEY `userid_idx` (`id_user`),
  KEY `keywordid_idx` (`id_keyword`),
  CONSTRAINT `collection_record_keywordid` FOREIGN KEY (`id_keyword`) REFERENCES `tb_keyword` (`id_keyword`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `collection_record_userid` FOREIGN KEY (`id_user`) REFERENCES `tb_user` (`id_user`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_collection_record`
--

LOCK TABLES `tb_collection_record` WRITE;
/*!40000 ALTER TABLE `tb_collection_record` DISABLE KEYS */;
INSERT INTO `tb_collection_record` VALUES (1,1,22,'Y',5,'2023-07-21'),(2,1,3,'Y',5,'2023-07-21'),(3,2,21,'Y',5,'2023-07-21'),(4,2,20,'Y',5,'2023-07-21'),(5,3,6,'Y',5,'2023-07-21'),(6,4,23,'Y',5,'2023-07-21'),(7,4,24,'Y',5,'2023-07-21'),(8,5,17,'Y',5,'2023-07-21'),(9,5,24,'Y',5,'2023-07-21');
/*!40000 ALTER TABLE `tb_collection_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_keyword`
--

DROP TABLE IF EXISTS `tb_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_keyword` (
  `id_keyword` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id_keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_keyword`
--

LOCK TABLES `tb_keyword` WRITE;
/*!40000 ALTER TABLE `tb_keyword` DISABLE KEYS */;
INSERT INTO `tb_keyword` VALUES (1,'癌症'),(2,'登革熱'),(3,'治療'),(4,'中國'),(5,'美國'),(6,'韓國'),(7,'電影'),(8,'韓勝宇'),(9,'梁朝偉'),(10,'颱風'),(11,'幼兒園'),(12,'杜蘇芮'),(13,'侯友宜'),(14,'國民黨'),(15,'民進黨'),(16,'亞太'),(17,'iphone'),(18,'電信'),(19,'股價'),(20,'台股'),(21,'台積電'),(22,'大谷翔平'),(23,'大聯盟'),(24,'nba'),(25,'南韓'),(26,'全壘打'),(27,'天使');
/*!40000 ALTER TABLE `tb_keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_news_score`
--

DROP TABLE IF EXISTS `tb_news_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_news_score` (
  `id_news_score` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_news` varchar(400) CHARACTER SET latin1 NOT NULL,
  `news_topic` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`id_news_score`),
  KEY `userid_idx` (`id_user`),
  CONSTRAINT `news_score_userid` FOREIGN KEY (`id_user`) REFERENCES `tb_user` (`id_user`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_news_score`
--

LOCK TABLES `tb_news_score` WRITE;
/*!40000 ALTER TABLE `tb_news_score` DISABLE KEYS */;
INSERT INTO `tb_news_score` VALUES (13,1,'6488c529bcfdc1a41d416f97','健康',5),(14,1,'6487982de5ad5e914341d456','健康',3),(15,1,'6483e9bc27f66f0727cedf56','運動',4),(16,2,'64946b665ab6cf5f7dcb8a5c','財經',4),(17,2,'64946b7c5ab6cf5f7dcb8aaa','財經',5),(18,2,'64946b925ab6cf5f7dcb8af6','財經',3),(19,3,'64871162e5ad5e914341cf32','娛樂',3),(20,3,'64871309e5ad5e914341cf42','娛樂',4),(21,3,'648ad6f53096230490d7c266','娛樂',5),(22,4,'6484a126f3cb64661cda7fa0','運動',2),(23,4,'64903e6595d2483a7919130d','運動',2),(24,4,'64884cd58318480204499712','運動',1);
/*!40000 ALTER TABLE `tb_news_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_ptt`
--

DROP TABLE IF EXISTS `tb_ptt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_ptt` (
  `id_ptt` int(11) NOT NULL AUTO_INCREMENT,
  `id_ptt_subtopic` int(11) NOT NULL,
  `title` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `ptt_url` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `date` date NOT NULL,
  `page` int(11) NOT NULL,
  PRIMARY KEY (`id_ptt`),
  KEY `ptt_subtopic_idx` (`id_ptt_subtopic`),
  CONSTRAINT `ptt_id_ptt_subtopic` FOREIGN KEY (`id_ptt_subtopic`) REFERENCES `tb_ptt_topic` (`id_ptt_subtopic`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_ptt`
--

LOCK TABLES `tb_ptt` WRITE;
/*!40000 ALTER TABLE `tb_ptt` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_ptt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_ptt_topic`
--

DROP TABLE IF EXISTS `tb_ptt_topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_ptt_topic` (
  `id_ptt_url` int(11) NOT NULL,
  `subtopic` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `ptt_url` varchar(400) CHARACTER SET latin1 NOT NULL,
  `page` int(11) NOT NULL,
  `id_ptt_subtopic` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_ptt_subtopic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_ptt_topic`
--

LOCK TABLES `tb_ptt_topic` WRITE;
/*!40000 ALTER TABLE `tb_ptt_topic` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_ptt_topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user`
--

DROP TABLE IF EXISTS `tb_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_user` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(200) CHARACTER SET latin1 NOT NULL,
  `password` varchar(200) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (1,'109403541@gmail.com','pbkdf2:sha256:600000$qTeVnOWhgHjy8hRb$4d90ede8158f862a41f90f58903f4a5db81e879e04cd0981ce6fdcc5868ec3ab'),(2,'109403502@gmail.com','pbkdf2:sha256:600000$q274hsvql7nLi2hQ$ec4f78ea22dfbff48192c7be605913a3aa24b59982b68044ae0071276441925f'),(3,'109403503@gmail.com','pbkdf2:sha256:600000$jRAHxBNiLsakuQrL$965df9563c32d9a3c1f7de47d8a4f295163d08b4fde3ec7c89046072a71fbdf3'),(4,'109403025@gmail.com','pbkdf2:sha256:600000$s8MQ5FzZESVgDeqj$bde6b58e315d390e15f8792a4d11655c9109e97dea6909087c5e342d539d255d'),(5,'109403516@gmail.com','pbkdf2:sha256:600000$dqymVLMaNiJ9BpP4$f7994561d05a06d5c823a05a8646c8140d3104862be336c2343dbe0aebbc4c32');
/*!40000 ALTER TABLE `tb_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-24 21:19:36
