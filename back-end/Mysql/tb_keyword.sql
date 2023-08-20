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
-- Table structure for table `tb_keyword`
--

DROP TABLE IF EXISTS `tb_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_keyword` (
  `id_keyword` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id_keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_keyword`
--

LOCK TABLES `tb_keyword` WRITE;
/*!40000 ALTER TABLE `tb_keyword` DISABLE KEYS */;
INSERT INTO `tb_keyword` VALUES (1,'癌症'),(2,'登革熱'),(3,'治療'),(4,'中國'),(5,'美國'),(6,'韓國'),(7,'電影'),(8,'韓勝宇'),(9,'梁朝偉'),(10,'颱風'),(11,'幼兒園'),(12,'杜蘇芮'),(13,'侯友宜'),(14,'國民黨'),(15,'民進黨'),(16,'亞太'),(17,'iphone'),(18,'電信'),(19,'股價'),(20,'台股'),(21,'台積電'),(22,'大谷翔平'),(23,'大聯盟'),(24,'nba'),(25,'南韓'),(26,'全壘打'),(27,'天使'),(28,'韓國瑜'),(29,'柯文哲'),(30,'投手'),(31,'紅襪'),(32,'安打'),(33,'二壘'),(34,'大谷'),(35,'選秀'),(36,'韓哥'),(37,'陳凱倫'),(38,'謝淑薇'),(39,'演唱會'),(40,'新歌'),(41,'女團'),(42,'歐陽妮妮'),(43,'王力宏'),(44,'導演'),(45,'魏德聖'),(46,'芭比'),(47,'蘋果'),(48,'秦剛'),(49,'防颱'),(50,'明星賽'),(51,'中華隊'),(52,'俄羅斯'),(53,'烏克蘭'),(54,'印度'),(55,'世界盃'),(56,'李登輝'),(57,'麟洋配'),(58,'德國'),(59,'羅志祥'),(60,'李玟'),(61,'楊紫瓊'),(62,'開唱'),(63,'吳東諺'),(64,'日本'),(65,'中共'),(66,'北韓'),(67,'歐洲'),(68,'氣象局'),(69,'颱風假'),(70,'太空人'),(71,'聯盟'),(72,'韋蘭德'),(73,'瓦德茲'),(74,'棒球'),(75,'緯創'),(76,'權值股'),(77,'大漲'),(78,'分析師'),(79,'氣象'),(80,'教師'),(81,'暴風圈'),(82,'卡努'),(83,'桃園'),(84,'中颱'),(85,'風雨'),(86,'彭名揚'),(87,'籃球'),(88,'阿拉薩'),(89,'美股'),(90,'新台幣'),(91,'外匯存底'),(92,'指數'),(93,'漲幅'),(94,'漲跌幅'),(95,'下跌'),(96,'u12'),(97,'男籃'),(98,'沙波尼斯'),(99,'美國隊'),(100,'梁恩碩'),(101,'麵包'),(102,'越南'),(103,'田馥甄'),(104,'楊亞依'),(105,'總教練'),(106,'網球'),(107,'白襪'),(108,'ai股'),(109,'熱門股'),(110,'概念股'),(111,'林憲銘'),(112,'陳傑憲'),(113,'統一'),(114,'敏感'),(115,'蘇智傑'),(116,'轉跌'),(117,'轉投資'),(118,'統一獅隊'),(119,'猛獅');
/*!40000 ALTER TABLE `tb_keyword` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-18 19:45:31
