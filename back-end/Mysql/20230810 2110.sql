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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_collection_record`
--

LOCK TABLES `tb_collection_record` WRITE;
/*!40000 ALTER TABLE `tb_collection_record` DISABLE KEYS */;
INSERT INTO `tb_collection_record` VALUES (1,1,22,'Y',5,'2023-07-21'),(2,1,3,'Y',5,'2023-07-21'),(3,2,21,'Y',5,'2023-07-21'),(4,2,20,'N',5,'2023-08-04'),(5,3,6,'Y',5,'2023-07-21'),(6,4,23,'Y',5,'2023-07-21'),(7,4,24,'Y',5,'2023-07-21'),(8,5,17,'Y',5,'2023-07-21'),(9,5,24,'Y',5,'2023-07-21'),(10,2,12,'N',5,'2023-08-04'),(11,2,50,'Y',5,'2023-08-03'),(12,2,51,'Y',5,'2023-08-03'),(13,2,79,'Y',5,'2023-08-03'),(14,2,22,'Y',5,'2023-08-05'),(15,2,10,'Y',5,'2023-08-07');
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
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_keyword`
--

LOCK TABLES `tb_keyword` WRITE;
/*!40000 ALTER TABLE `tb_keyword` DISABLE KEYS */;
INSERT INTO `tb_keyword` VALUES (1,'癌症'),(2,'登革熱'),(3,'治療'),(4,'中國'),(5,'美國'),(6,'韓國'),(7,'電影'),(8,'韓勝宇'),(9,'梁朝偉'),(10,'颱風'),(11,'幼兒園'),(12,'杜蘇芮'),(13,'侯友宜'),(14,'國民黨'),(15,'民進黨'),(16,'亞太'),(17,'iphone'),(18,'電信'),(19,'股價'),(20,'台股'),(21,'台積電'),(22,'大谷翔平'),(23,'大聯盟'),(24,'nba'),(25,'南韓'),(26,'全壘打'),(27,'天使'),(28,'韓國瑜'),(29,'柯文哲'),(30,'投手'),(31,'紅襪'),(32,'安打'),(33,'二壘'),(34,'大谷'),(35,'選秀'),(36,'韓哥'),(37,'陳凱倫'),(38,'謝淑薇'),(39,'演唱會'),(40,'新歌'),(41,'女團'),(42,'歐陽妮妮'),(43,'王力宏'),(44,'導演'),(45,'魏德聖'),(46,'芭比'),(47,'蘋果'),(48,'秦剛'),(49,'防颱'),(50,'明星賽'),(51,'中華隊'),(52,'明'),(53,'星'),(54,'賽'),(55,'俄羅斯'),(56,'烏克蘭'),(57,'印度'),(58,'世界盃'),(59,'李登輝'),(60,'麟洋配'),(61,'德國'),(62,'羅志祥'),(63,'李玟'),(64,'楊紫瓊'),(65,'開唱'),(66,'吳東諺'),(67,'3'),(68,'日本'),(69,'中共'),(70,'北韓'),(71,'歐洲'),(72,'氣象局'),(73,'颱風假'),(74,'太空人'),(75,'聯盟'),(76,'韋蘭德'),(77,'瓦德茲'),(78,'棒球'),(79,'緯創'),(80,'權值股'),(81,'大漲'),(82,'分析師'),(83,'氣象'),(84,'教師'),(85,'暴風圈'),(86,'卡努'),(87,'桃園'),(88,'中颱'),(89,'風雨'),(90,'彭名揚'),(91,'籃球'),(92,'阿拉薩'),(93,'美股'),(94,'新台幣'),(95,'外匯存底'),(96,'指數'),(97,'漲幅'),(98,'漲跌幅'),(99,'下跌'),(100,'u12'),(101,'男籃'),(102,'沙波尼斯'),(103,'美國隊'),(104,'梁恩碩'),(105,'麵包'),(106,'越南'),(107,'田馥甄'),(108,'楊亞依'),(109,'總教練'),(110,'網球'),(111,'白襪'),(112,'ai股'),(113,'熱門股'),(114,'概念股'),(115,'林憲銘'),(116,'陳傑憲'),(117,'統一'),(118,'敏感'),(119,'蘇智傑'),(120,'猛'),(121,'獅'),(122,'轉跌'),(123,'轉投資'),(124,'統一獅隊'),(125,'緯'),(126,'創'),(127,'猛獅');
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_news_score`
--

LOCK TABLES `tb_news_score` WRITE;
/*!40000 ALTER TABLE `tb_news_score` DISABLE KEYS */;
INSERT INTO `tb_news_score` VALUES (13,1,'6488c529bcfdc1a41d416f97','健康',5),(14,1,'6487982de5ad5e914341d456','健康',3),(15,1,'6483e9bc27f66f0727cedf56','運動',4),(16,2,'64946b665ab6cf5f7dcb8a5c','財經',4),(17,2,'64946b7c5ab6cf5f7dcb8aaa','財經',5),(18,2,'64946b925ab6cf5f7dcb8af6','財經',3),(19,3,'64871162e5ad5e914341cf32','娛樂',3),(20,3,'64871309e5ad5e914341cf42','娛樂',4),(21,3,'648ad6f53096230490d7c266','娛樂',5),(22,4,'6484a126f3cb64661cda7fa0','運動',2),(23,4,'64903e6595d2483a7919130d','運動',2),(24,4,'64884cd58318480204499712','運動',1),(25,2,'64c71c56fced6ee39afb7754','運動 ',5),(26,2,'64c71c29fced6ee39afb6fec','社會地方 ',5),(27,2,'64c71c56fced6ee39afb7737','運動 ',5),(28,2,'64cac1978a08f8cce779e596','生活 ',5),(29,2,'64cac18a8a08f8cce779e30e','運動 ',5),(30,2,'64cac18c8a08f8cce779e362','運動 ',1),(31,2,'64cac1778a08f8cce779df9b','財經 ',1),(32,2,'64baec8d977fd234c3509577','財經 ',5),(33,2,'64901a1b54e0e79a58bc279d','運動 ',5),(34,2,'64cac1948a08f8cce779e4e2','運動 ',0),(35,2,'64cff8009ef0e215153388f7','健康 ',0),(36,2,'64cc19aae89cda559e964a44','生活 ',5);
/*!40000 ALTER TABLE `tb_news_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_ptt_data`
--

DROP TABLE IF EXISTS `tb_ptt_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_ptt_data` (
  `id_ptt_data` int(11) NOT NULL AUTO_INCREMENT,
  `subtopic` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` varchar(400) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `page` int(11) NOT NULL,
  PRIMARY KEY (`id_ptt_data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_ptt_data`
--

LOCK TABLES `tb_ptt_data` WRITE;
/*!40000 ALTER TABLE `tb_ptt_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_ptt_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_ptt_search_link`
--

DROP TABLE IF EXISTS `tb_ptt_search_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_ptt_search_link` (
  `id_ptt_link` int(11) NOT NULL,
  `id_subtopic` int(11) NOT NULL,
  `ptt_url` varchar(400) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subtopic` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `page` int(11) NOT NULL,
  PRIMARY KEY (`id_ptt_link`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_ptt_search_link`
--

LOCK TABLES `tb_ptt_search_link` WRITE;
/*!40000 ALTER TABLE `tb_ptt_search_link` DISABLE KEYS */;
INSERT INTO `tb_ptt_search_link` VALUES (1,1,'https://www.ptt.cc/bbs/Baseball/index.html','棒球',13950),(2,2,'https://www.ptt.cc/bbs/basketballTW/index.html','籃球',4006),(3,3,'https://www.ptt.cc/bbs/NBA/index.html','籃球',6507),(4,4,'https://www.ptt.cc/bbs/Tennis/index.html','網球',2322),(5,5,'https://www.ptt.cc/bbs/Golf/index.html','高爾夫球',534),(6,6,'https://www.ptt.cc/bbs/Food/index.html','美食消費',7004),(7,7,'https://www.ptt.cc/bbs/travel/index.html','旅遊交通',3075),(8,8,'https://www.ptt.cc/bbs/Education/index.html','文教',459),(9,9,'https://www.ptt.cc/bbs/Boy-Girl/index.html','兩性親子',6231),(10,10,'https://www.ptt.cc/bbs/KR_Entertain/index.html','日韓娛樂',2275),(11,11,'https://www.ptt.cc/bbs/TW_Entertain/index.html','藝人動態',1136),(12,12,'https://www.ptt.cc/bbs/music/index.html','音樂',759),(13,13,'https://www.ptt.cc/bbs/movie/index.html','電影戲劇',9624),(14,14,'https://www.ptt.cc/bbs/Drama/index.html','電影戲劇',1225),(15,15,'https://www.ptt.cc/bbs/Tech_Job/index.html','科技新知',4002),(16,16,'https://www.ptt.cc/bbs/Mobile-game/index.html','遊戲相關',1018),(17,17,'https://www.ptt.cc/bbs/Steam/index.html','遊戲相關',3680),(18,18,'https://www.ptt.cc/bbs/E-appliance/index.html','3C家電',1837),(19,19,'https://www.ptt.cc/bbs/iOS/index.html','手機iOS',5400),(20,20,'https://www.ptt.cc/bbs/Android/index.html','手機Android',2386),(21,21,'https://www.ptt.cc/bbs/regimen/index.html','養生飲食',2385),(22,22,'https://www.ptt.cc/bbs/Anti-Cancer/index.html','癌症',1029),(23,23,'https://www.ptt.cc/bbs/FITNESS/index.html','塑身減重',1571),(24,24,'https://www.ptt.cc/bbs/Health/index.html','慢性病',442),(25,25,'https://www.ptt.cc/bbs/IA/index.html','亞澳',3585),(26,26,'https://www.ptt.cc/bbs/IA/index.html','中港澳',3585),(27,27,'https://www.ptt.cc/bbs/IA/index.html','美洲',3585),(28,28,'https://www.ptt.cc/bbs/IA/index.html','歐非',3585),(29,29,'https://www.ptt.cc/bbs/TY_Research/index.html','氣象',1333),(30,30,'https://www.ptt.cc/bbs/Gossiping/index.html','新奇',39455),(31,31,'https://www.ptt.cc/bbs/Gossiping/index.html','大台北',39455),(32,32,'https://www.ptt.cc/bbs/Gossiping/index.html','北台灣',39455),(33,33,'https://www.ptt.cc/bbs/Gossiping/index.html','中部離島',39455),(34,34,'https://www.ptt.cc/bbs/Gossiping/index.html','南台灣',39455),(35,35,'https://www.ptt.cc/bbs/Gossiping/index.html','東台灣',39455),(36,36,'https://www.ptt.cc/bbs/Tech_Job/index.html','科技新知',4002),(37,37,'https://www.ptt.cc/bbs/Stock/index.html','股市匯市',6377),(38,38,'https://www.ptt.cc/bbs/home-sale/index.html','房地產',5018),(39,39,'https://www.ptt.cc/bbs/Gossiping/index.html','產業動態',39455),(40,40,'https://www.ptt.cc/bbs/Football/index.html','足球 ',1093),(41,41,'https://www.ptt.cc/bbs/Volleyball/index.html','排球',1220),(42,42,'https://www.ptt.cc/bbs/Track_Field/index.html','田徑',25),(43,43,'https://www.ptt.cc/bbs/Baseball/index.html','中職',13907),(44,44,'https://www.ptt.cc/bbs/MLB/index.html','MLB',2134),(45,45,'https://www.ptt.cc/bbs/Elephants/index.html','中信兄弟',5274),(46,46,'https://www.ptt.cc/bbs/WCDragons/index.html','味全龍',394),(47,47,'https://www.ptt.cc/bbs/Lions/index.html','統一獅',4155),(48,48,'https://www.ptt.cc/bbs/Guardians/index.html','富邦悍將',4061),(49,49,'https://www.ptt.cc/bbs/TSG-Hawks/index.html','台鋼雄鷹',40),(50,50,'https://www.ptt.cc/bbs/Baseball/index.html','日職',13950),(51,51,'https://www.ptt.cc/bbs/K_baseball/index.html','韓職',262),(52,52,'https://www.ptt.cc/bbs/MLB/index.html','MLB 洋基',2134),(53,53,'https://www.ptt.cc/bbs/MLB/index.html','MLB 紅襪',2134),(54,54,'https://www.ptt.cc/bbs/MLB/index.html','MLB 光芒',2134),(55,55,'https://www.ptt.cc/bbs/MLB/index.html','MLB 金鶯',2134),(56,56,'https://www.ptt.cc/bbs/MLB/index.html','MLB 藍鳥',2134),(57,57,'https://www.ptt.cc/bbs/MLB/index.html','MLB 守護者',2134),(58,58,'https://www.ptt.cc/bbs/MLB/index.html','MLB 白襪',2134),(59,59,'https://www.ptt.cc/bbs/MLB/index.html','MLB 皇家',2134),(60,60,'https://www.ptt.cc/bbs/MLB/index.html','MLB 老虎',2134),(61,61,'https://www.ptt.cc/bbs/MLB/index.html','MLB 雙城',2134),(62,62,'https://www.ptt.cc/bbs/MLB/index.html','MLB 太空人',2134),(63,63,'https://www.ptt.cc/bbs/MLB/index.html','MLB 運動家',2134),(64,64,'https://www.ptt.cc/bbs/MLB/index.html','MLB 水手',2134),(65,65,'https://www.ptt.cc/bbs/MLB/index.html','MLB 天使',2134),(66,66,'https://www.ptt.cc/bbs/MLB/index.html','MLB 遊騎兵',2134),(67,67,'https://www.ptt.cc/bbs/MLB/index.html','MLB 大都會',2134),(68,68,'https://www.ptt.cc/bbs/MLB/index.html','MLB 勇士',2134),(69,69,'https://www.ptt.cc/bbs/MLB/index.html','MLB 費城人',2134),(70,70,'https://www.ptt.cc/bbs/MLB/index.html','MLB 馬林魚',2134),(71,71,'https://www.ptt.cc/bbs/MLB/index.html','MLB 國民',2134),(72,72,'https://www.ptt.cc/bbs/MLB/index.html','MLB 釀酒人',2134),(73,73,'https://www.ptt.cc/bbs/MLB/index.html','MLB 紅雀',2134),(74,74,'https://www.ptt.cc/bbs/MLB/index.html','MLB 紅人',2134),(75,75,'https://www.ptt.cc/bbs/MLB/index.html','MLB 小熊',2134),(76,76,'https://www.ptt.cc/bbs/MLB/index.html','MLB 海盜',2134),(77,77,'https://www.ptt.cc/bbs/MLB/index.html','MLB 響尾蛇',2134),(78,78,'https://www.ptt.cc/bbs/MLB/index.html','MLB 道奇',2134),(79,79,'https://www.ptt.cc/bbs/MLB/index.html','MLB 落磯',2134),(80,80,'https://www.ptt.cc/bbs/MLB/index.html','MLB 巨人',2134),(81,81,'https://www.ptt.cc/bbs/MLB/index.html','MLB 教士',2134),(82,82,'https://www.ptt.cc/bbs/NBA/index.html','NBA',6503),(83,83,'https://www.ptt.cc/bbs/NBA/index.html','波士頓塞爾蒂克',6503),(84,84,'https://www.ptt.cc/bbs/NBA/index.html','布魯克林籃網',6503),(85,85,'https://www.ptt.cc/bbs/NBA/index.html','紐約尼克',6503),(86,86,'https://www.ptt.cc/bbs/NBA/index.html','費城76人',6503),(87,87,'https://www.ptt.cc/bbs/NBA/index.html','多倫多暴龍',6503),(88,88,'https://www.ptt.cc/bbs/NBA/index.html','芝加哥公牛',6503),(89,89,'https://www.ptt.cc/bbs/NBA/index.html','克里夫蘭騎士',6503),(90,90,'https://www.ptt.cc/bbs/NBA/index.html','底特律活塞',6503),(91,91,'https://www.ptt.cc/bbs/NBA/index.html','印第安那溜馬',6503),(92,92,'https://www.ptt.cc/bbs/NBA/index.html','密爾瓦基公鹿',6503),(93,93,'https://www.ptt.cc/bbs/NBA/index.html','亞特蘭大老鷹',6503),(94,94,'https://www.ptt.cc/bbs/NBA/index.html','夏洛特黃蜂',6503),(95,95,'https://www.ptt.cc/bbs/NBA/index.html','邁阿密熱火',6503),(96,96,'https://www.ptt.cc/bbs/NBA/index.html','奧蘭多魔術',6503),(97,97,'https://www.ptt.cc/bbs/NBA/index.html','華盛頓巫師',6503),(98,98,'https://www.ptt.cc/bbs/NBA/index.html','金州勇士',6503),(99,99,'https://www.ptt.cc/bbs/NBA/index.html','洛杉磯快艇',6503),(100,100,'https://www.ptt.cc/bbs/NBA/index.html','洛杉磯湖人',6503),(101,101,'https://www.ptt.cc/bbs/NBA/index.html','鳳凰城太陽',6503),(102,102,'https://www.ptt.cc/bbs/NBA/index.html','沙加緬度國王',6503),(103,103,'https://www.ptt.cc/bbs/NBA/index.html','丹佛金塊',6503),(104,104,'https://www.ptt.cc/bbs/NBA/index.html','明尼蘇達灰狼',6503),(105,105,'https://www.ptt.cc/bbs/NBA/index.html','奧克拉荷馬雷霆',6503),(106,106,'https://www.ptt.cc/bbs/NBA/index.html','波特蘭拓荒者',6503),(107,107,'https://www.ptt.cc/bbs/NBA/index.html','猶他爵士',6503),(108,108,'https://www.ptt.cc/bbs/NBA/index.html','達拉斯獨行俠',6503),(109,109,'https://www.ptt.cc/bbs/NBA/index.html','休士頓火箭',6503),(110,110,'https://www.ptt.cc/bbs/NBA/index.html','曼斐斯灰熊',6503),(111,111,'https://www.ptt.cc/bbs/NBA/index.html','紐奧良鵜鶘',6503),(112,112,'https://www.ptt.cc/bbs/NBA/index.html','聖安東尼奧馬刺',6503),(113,113,'https://www.ptt.cc/bbs/basketballTW/index.html','PLG',4003),(114,114,'https://www.ptt.cc/bbs/basketballTW/index.html','新北國王',4003),(115,115,'https://www.ptt.cc/bbs/basketballTW/index.html','臺北富邦勇士',4003),(116,116,'https://www.ptt.cc/bbs/basketballTW/index.html','桃園璞園領航猿',4003),(117,117,'https://www.ptt.cc/bbs/basketballTW/index.html','福爾摩沙台新夢想家',4003),(118,118,'https://www.ptt.cc/bbs/basketballTW/index.html','高雄17直播鋼鐵人',4003),(119,119,'https://www.ptt.cc/bbs/basketballTW/index.html','新竹街口攻城獅',4003),(120,120,'https://www.ptt.cc/bbs/basketballTW/index.html','T1',4003),(121,121,'https://www.ptt.cc/bbs/basketballTW/index.html','新北中信特攻',4003),(122,122,'https://www.ptt.cc/bbs/basketballTW/index.html','臺南台鋼獵鷹',4003),(123,123,'https://www.ptt.cc/bbs/basketballTW/index.html','高雄全家海神',4003),(124,124,'https://www.ptt.cc/bbs/basketballTW/index.html','台灣啤酒英熊',4003),(125,125,'https://www.ptt.cc/bbs/basketballTW/index.html','臺中太陽',4003),(126,126,'https://www.ptt.cc/bbs/basketballTW/index.html','桃園永豐雲豹',4003);
/*!40000 ALTER TABLE `tb_ptt_search_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_subtopic`
--

DROP TABLE IF EXISTS `tb_subtopic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_subtopic` (
  `id_subtopic` int(11) NOT NULL,
  `subtopic_value` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_subtopic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_subtopic`
--

LOCK TABLES `tb_subtopic` WRITE;
/*!40000 ALTER TABLE `tb_subtopic` DISABLE KEYS */;
INSERT INTO `tb_subtopic` VALUES (1,'棒球'),(2,'籃球'),(3,'籃球'),(4,'網球'),(5,'高爾夫球'),(6,'美食消費'),(7,'旅遊交通'),(8,'文教'),(9,'兩性親子'),(10,'日韓娛樂'),(11,'藝人動態'),(12,'音樂'),(13,'電影戲劇'),(14,'電影戲劇'),(15,'科技新知'),(16,'遊戲相關'),(17,'遊戲相關'),(18,'3C家電'),(19,'手機iOS'),(20,'手機Android'),(21,'養生飲食'),(22,'癌症'),(23,'塑身減重'),(24,'慢性病'),(25,'亞澳'),(26,'中港澳'),(27,'美洲'),(28,'歐非'),(29,'氣象'),(30,'新奇'),(31,'大台北'),(32,'北台灣'),(33,'中部離島'),(34,'南台灣'),(35,'東台灣'),(36,'科技新知'),(37,'股市匯市'),(38,'房地產'),(39,'產業動態'),(40,'足球 '),(41,'排球'),(42,'田徑'),(43,'中職'),(44,'MLB'),(45,'中信兄弟'),(46,'味全龍'),(47,'統一獅'),(48,'富邦悍將'),(49,'台鋼雄鷹'),(50,'日職'),(51,'韓職'),(52,'MLB 洋基'),(53,'MLB 紅襪'),(54,'MLB 光芒'),(55,'MLB 金鶯'),(56,'MLB 藍鳥'),(57,'MLB 守護者'),(58,'MLB 白襪'),(59,'MLB 皇家'),(60,'MLB 老虎'),(61,'MLB 雙城'),(62,'MLB 太空人'),(63,'MLB 運動家'),(64,'MLB 水手'),(65,'MLB 天使'),(66,'MLB 遊騎兵'),(67,'MLB 大都會'),(68,'MLB 勇士'),(69,'MLB 費城人'),(70,'MLB 馬林魚'),(71,'MLB 國民'),(72,'MLB 釀酒人'),(73,'MLB 紅雀'),(74,'MLB 紅人'),(75,'MLB 小熊'),(76,'MLB 海盜'),(77,'MLB 響尾蛇'),(78,'MLB 道奇'),(79,'MLB 落磯'),(80,'MLB 巨人'),(81,'MLB 教士'),(82,'NBA'),(83,'波士頓塞爾蒂克'),(84,'布魯克林籃網'),(85,'紐約尼克'),(86,'費城76人'),(87,'多倫多暴龍'),(88,'芝加哥公牛'),(89,'克里夫蘭騎士'),(90,'底特律活塞'),(91,'印第安那溜馬'),(92,'密爾瓦基公鹿'),(93,'亞特蘭大老鷹'),(94,'夏洛特黃蜂'),(95,'邁阿密熱火'),(96,'奧蘭多魔術'),(97,'華盛頓巫師'),(98,'金州勇士'),(99,'洛杉磯快艇'),(100,'洛杉磯湖人'),(101,'鳳凰城太陽'),(102,'沙加緬度國王'),(103,'丹佛金塊'),(104,'明尼蘇達灰狼'),(105,'奧克拉荷馬雷霆'),(106,'波特蘭拓荒者'),(107,'猶他爵士'),(108,'達拉斯獨行俠'),(109,'休士頓火箭'),(110,'曼斐斯灰熊'),(111,'紐奧良鵜鶘'),(112,'聖安東尼奧馬刺'),(113,'PLG'),(114,'新北國王'),(115,'臺北富邦勇士'),(116,'桃園璞園領航猿'),(117,'福爾摩沙台新夢想家'),(118,'高雄17直播鋼鐵人'),(119,'新竹街口攻城獅'),(120,'T1'),(121,'新北中信特攻'),(122,'臺南台鋼獵鷹'),(123,'高雄全家海神'),(124,'台灣啤酒英熊'),(125,'臺中太陽'),(126,'桃園永豐雲豹');
/*!40000 ALTER TABLE `tb_subtopic` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (1,'109403541@gmail.com','pbkdf2:sha256:600000$qTeVnOWhgHjy8hRb$4d90ede8158f862a41f90f58903f4a5db81e879e04cd0981ce6fdcc5868ec3ab'),(2,'109403502@gmail.com','pbkdf2:sha256:600000$q274hsvql7nLi2hQ$ec4f78ea22dfbff48192c7be605913a3aa24b59982b68044ae0071276441925f'),(3,'109403503@gmail.com','pbkdf2:sha256:600000$jRAHxBNiLsakuQrL$965df9563c32d9a3c1f7de47d8a4f295163d08b4fde3ec7c89046072a71fbdf3'),(4,'109403025@gmail.com','pbkdf2:sha256:600000$s8MQ5FzZESVgDeqj$bde6b58e315d390e15f8792a4d11655c9109e97dea6909087c5e342d539d255d'),(5,'109403516@gmail.com','pbkdf2:sha256:600000$dqymVLMaNiJ9BpP4$f7994561d05a06d5c823a05a8646c8140d3104862be336c2343dbe0aebbc4c32'),(6,'WAWA@gmail.com','pbkdf2:sha256:600000$clkPCBaBbD2el3Vu$05a2f622d2e27c0814867b00ca6a0e5176efd7126955ff907bd7719eacdcd4ab');
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

-- Dump completed on 2023-08-10 19:10:40
