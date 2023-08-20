CREATE DATABASE  IF NOT EXISTS `communews` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `communews`;
-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: communews.ctqdwhl8sobn.us-east-1.rds.amazonaws.com    Database: communews
-- ------------------------------------------------------
-- Server version	8.0.33

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `tb_subtopic`
--

DROP TABLE IF EXISTS `tb_subtopic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_subtopic` (
  `id_subtopic` int NOT NULL,
  `subtopic_value` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `topic` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_subtopic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_subtopic`
--

LOCK TABLES `tb_subtopic` WRITE;
/*!40000 ALTER TABLE `tb_subtopic` DISABLE KEYS */;
INSERT INTO `tb_subtopic` VALUES (1,'棒球','運動'),(2,'籃球','運動'),(3,'籃球','運動'),(4,'網球','運動'),(5,'高爾夫球','運動'),(6,'美食消費','生活'),(7,'旅遊交通','生活'),(8,'文教','生活'),(9,'兩性親子','生活'),(10,'日韓娛樂','娛樂'),(11,'藝人動態','娛樂'),(12,'音樂','娛樂'),(13,'電影戲劇','娛樂'),(14,'電影戲劇','娛樂'),(15,'科技新知','科技'),(16,'遊戲相關','科技'),(17,'遊戲相關','科技'),(18,'3C家電','科技'),(19,'手機iOS','科技'),(20,'手機Android','科技'),(21,'養生飲食','健康'),(22,'癌症','健康'),(23,'塑身減重','健康'),(24,'慢性病','健康'),(25,'亞澳','國際'),(26,'中港澳','國際'),(27,'美洲','國際'),(28,'歐非','國際'),(29,'氣象','生活'),(30,'新奇','生活'),(31,'大台北','社會地方'),(32,'北台灣','社會地方'),(33,'中部離島','社會地方'),(34,'南台灣','社會地方'),(35,'東台灣','社會地方'),(36,'科技新知','科技'),(37,'股市匯市','財經'),(38,'房地產','財經'),(39,'產業動態','財經'),(40,'足球 ','運動'),(41,'排球','運動'),(42,'田徑','運動'),(43,'中職','運動'),(44,'MLB','運動'),(45,'中信兄弟','運動'),(46,'味全龍','運動'),(47,'統一獅','運動'),(48,'富邦悍將','運動'),(49,'台鋼雄鷹','運動'),(50,'日職','運動'),(51,'韓職','運動'),(52,'MLB 洋基','運動'),(53,'MLB 紅襪','運動'),(54,'MLB 光芒','運動'),(55,'MLB 金鶯','運動'),(56,'MLB 藍鳥','運動'),(57,'MLB 守護者','運動'),(58,'MLB 白襪','運動'),(59,'MLB 皇家','運動'),(60,'MLB 老虎','運動'),(61,'MLB 雙城','運動'),(62,'MLB 太空人','運動'),(63,'MLB 運動家','運動'),(64,'MLB 水手','運動'),(65,'MLB 天使','運動'),(66,'MLB 遊騎兵','運動'),(67,'MLB 大都會','運動'),(68,'MLB 勇士','運動'),(69,'MLB 費城人','運動'),(70,'MLB 馬林魚','運動'),(71,'MLB 國民','運動'),(72,'MLB 釀酒人','運動'),(73,'MLB 紅雀','運動'),(74,'MLB 紅人','運動'),(75,'MLB 小熊','運動'),(76,'MLB 海盜','運動'),(77,'MLB 響尾蛇','運動'),(78,'MLB 道奇','運動'),(79,'MLB 落磯','運動'),(80,'MLB 巨人','運動'),(81,'MLB 教士','運動'),(82,'NBA','運動'),(83,'波士頓塞爾蒂克','運動'),(84,'布魯克林籃網','運動'),(85,'紐約尼克','運動'),(86,'費城76人','運動'),(87,'多倫多暴龍','運動'),(88,'芝加哥公牛','運動'),(89,'克里夫蘭騎士','運動'),(90,'底特律活塞','運動'),(91,'印第安那溜馬','運動'),(92,'密爾瓦基公鹿','運動'),(93,'亞特蘭大老鷹','運動'),(94,'夏洛特黃蜂','運動'),(95,'邁阿密熱火','運動'),(96,'奧蘭多魔術','運動'),(97,'華盛頓巫師','運動'),(98,'金州勇士','運動'),(99,'洛杉磯快艇','運動'),(100,'洛杉磯湖人','運動'),(101,'鳳凰城太陽','運動'),(102,'沙加緬度國王','運動'),(103,'丹佛金塊','運動'),(104,'明尼蘇達灰狼','運動'),(105,'奧克拉荷馬雷霆','運動'),(106,'波特蘭拓荒者','運動'),(107,'猶他爵士','運動'),(108,'達拉斯獨行俠','運動'),(109,'休士頓火箭','運動'),(110,'曼斐斯灰熊','運動'),(111,'紐奧良鵜鶘','運動'),(112,'聖安東尼奧馬刺','運動'),(113,'PLG','運動'),(114,'新北國王','運動'),(115,'臺北富邦勇士','運動'),(116,'桃園璞園領航猿','運動'),(117,'福爾摩沙台新夢想家','運動'),(118,'高雄17直播鋼鐵人','運動'),(119,'新竹街口攻城獅','運動'),(120,'T1','運動'),(121,'新北中信特攻','運動'),(122,'臺南台鋼獵鷹','運動'),(123,'高雄全家海神','運動'),(124,'台灣啤酒英熊','運動'),(125,'臺中太陽','運動'),(126,'桃園永豐雲豹','運動');
/*!40000 ALTER TABLE `tb_subtopic` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-17 19:50:43
