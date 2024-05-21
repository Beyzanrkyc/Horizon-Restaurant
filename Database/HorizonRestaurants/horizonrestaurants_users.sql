CREATE DATABASE  IF NOT EXISTS `horizonrestaurants` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `horizonrestaurants`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: horizonrestaurants
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `restaurantId` int DEFAULT NULL,
  `userName` varchar(45) DEFAULT NULL,
  `password` varchar(72) DEFAULT NULL,
  `privilege` int DEFAULT NULL,
  `salt` varchar(72) DEFAULT NULL,
  PRIMARY KEY (`userId`),
  KEY `fk_Users_Resturant_idx` (`restaurantId`),
  CONSTRAINT `fk_Users_Resturant` FOREIGN KEY (`restaurantId`) REFERENCES `restaurants` (`restaurantId`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,1,'Manager','b\'$2b$12$Bp79LXLLhL8t3peefiuah.WpDOC8owqtsZ2az8OZn99M3P5IhpQa6\'',1,'b\'$2b$12$Bp79LXLLhL8t3peefiuah.\''),(2,1,'Staff','b\'$2b$12$Z5u4DBs4TPmH6LIzwoDJpOV6dKoQ8AR9cDZsxIVjXSp7785vLVfma\'',2,'b\'$2b$12$Z5u4DBs4TPmH6LIzwoDJpO\''),(3,2,'Manager','b\'$2b$12$qYkrFMfJ8OBDb/4v6qSR2eW9yt0KoYp/ME2YNznVFCX/Q0lhJKKrG\'',1,'b\'$2b$12$qYkrFMfJ8OBDb/4v6qSR2e\''),(4,2,'Staff','b\'$2b$12$aec.VIKd41PjJJK5Kc8K3eLFHs4.yUrw29tA89st400c.a5ocXZs2\'',2,'b\'$2b$12$aec.VIKd41PjJJK5Kc8K3e\''),(5,3,'Manager','b\'$2b$12$gi9wI2D4vi5UMkl9qWWF3O3r0IvtlvQ/IdZgebqTjbAoqhLJ6ev7K\'',1,'b\'$2b$12$gi9wI2D4vi5UMkl9qWWF3O\''),(6,3,'Staff','b\'$2b$12$lgktlyXSqTcPz9lLh6n/C.wQZHNKwagArFvQXRvLjoFdndyHQQFtO\'',2,'b\'$2b$12$lgktlyXSqTcPz9lLh6n/C.\''),(7,4,'Manager','b\'$2b$12$VZTJFgToWrQUrUWzQsjQTeMiBSif8z58NAXuBzFriLL6Yfw3Pyy0K\'',1,'b\'$2b$12$VZTJFgToWrQUrUWzQsjQTe\''),(8,4,'Staff','b\'$2b$12$GKnkd/gqC4wMvophYgOUV.pqLfpmB0uuHfNnKe7gnb5yKhyX/Z8MK\'',2,'b\'$2b$12$GKnkd/gqC4wMvophYgOUV.\''),(9,5,'Manager','b\'$2b$12$Z3nbU0k1xtHXlSBMxljtNePjdtPsFEm.RB6nv3ClYzdF1SZWHaX6.\'',1,'b\'$2b$12$Z3nbU0k1xtHXlSBMxljtNe\''),(10,5,'Staff','b\'$2b$12$B8SCegore1bA9YOBkOXblOPyuL0Oyhu7XphiqlunrK0wEHLQJ5Vbe\'',2,'b\'$2b$12$B8SCegore1bA9YOBkOXblO\''),(11,6,'Manager','b\'$2b$12$h2i8J1F8Gz3rM5yhaGJI/OxtmZfEQN.wAuEp5j9GzA6SFJe2MfcAy\'',1,'b\'$2b$12$h2i8J1F8Gz3rM5yhaGJI/O\''),(12,6,'Staff','b\'$2b$12$iQOgYoLhYtiZqZsHleFE8OiHajkK7z9W3hu.xlLPvIqQoB4GB8/wu\'',2,'b\'$2b$12$iQOgYoLhYtiZqZsHleFE8O\''),(13,7,'Manager','b\'$2b$12$/b3BNpaMSac86SnoH2H3ZeU4MurLDWdXBTGp7Dp8SnaWBnTUGkC8m\'',1,'b\'$2b$12$/b3BNpaMSac86SnoH2H3Ze\''),(14,7,'Staff','b\'$2b$12$seogCXvh1.xaPQ1jks4D0.kWi2Wgmt5V3v04ld1bebSfDntX4IBnu\'',2,'b\'$2b$12$seogCXvh1.xaPQ1jks4D0.\''),(15,8,'Manager','b\'$2b$12$W8R11m4zmVbFE4ajGsa71OIMepbM1AZFRJCySzA5nNsCKfkxuFC/a\'',1,'b\'$2b$12$W8R11m4zmVbFE4ajGsa71O\''),(16,8,'Staff','b\'$2b$12$Giprurd8ybnR.eY8VwQ9U.d/8RSqWoXGVXQdkBU2S65acVKKvHSw.\'',2,'b\'$2b$12$Giprurd8ybnR.eY8VwQ9U.\''),(17,9,'Manager','b\'$2b$12$k2GMecaW4P9mei08pLWWEO5ImoC5f2Omjj/PhHHnzB6xN6LVazesq\'',1,'b\'$2b$12$k2GMecaW4P9mei08pLWWEO\''),(18,9,'Staff','b\'$2b$12$pWMbe9er1J2uznPcOV1fTeY9MSt7kDgx2lMjfcDD8NsRrnZGIE1au\'',2,'b\'$2b$12$pWMbe9er1J2uznPcOV1fTe\''),(19,10,'Manager','b\'$2b$12$WppfF8KqTzusQX66.7AYI.nXSY0NzpB9EGUpMm3/I2hWoXK8m6W/2\'',1,'b\'$2b$12$WppfF8KqTzusQX66.7AYI.\''),(20,10,'Staff','b\'$2b$12$6WuP/FQ4aj/yevmdPLgQcuHgO2V3o7aqcuxLFP4K46zBAg5B69VJ.\'',2,'b\'$2b$12$6WuP/FQ4aj/yevmdPLgQcu\''),(21,11,'Manager','b\'$2b$12$u/8QV8/ryfMWVydhpIXBV.IZ3fRxUTEnwYlSUDoC7zsqn.UsW6R7W\'',1,'b\'$2b$12$u/8QV8/ryfMWVydhpIXBV.\''),(22,11,'Staff','b\'$2b$12$4R47Xi/uIHbO6OynDwqAJ.f7ci5Xr2UdYjzHIY0wXzev0bYJxKSdC\'',2,'b\'$2b$12$4R47Xi/uIHbO6OynDwqAJ.\''),(23,12,'Manager','b\'$2b$12$USfgxguzqT2RiMudWRw72.FCeAmweI5CXdqRAuCy58hmnYhr3LIE6\'',1,'b\'$2b$12$USfgxguzqT2RiMudWRw72.\''),(24,12,'Staff','b\'$2b$12$3KYuqe79sXRPde9yWL0SReTCTzqaPkVWu0tnGIX70sjQtQ9VBI9xa\'',2,'b\'$2b$12$3KYuqe79sXRPde9yWL0SRe\''),(25,13,'Manager','b\'$2b$12$BI6T3RCYunT9Y2OsnPR.bezkFOFiCJxC3EMJ1CZ48ojM3xq4lbQZa\'',1,'b\'$2b$12$BI6T3RCYunT9Y2OsnPR.be\''),(26,13,'Staff','b\'$2b$12$fzmq8k3zcGoP.tqytYeNV.5tsotWWEQmZrJm9.afnwlz3laT8ve66\'',2,'b\'$2b$12$fzmq8k3zcGoP.tqytYeNV.\''),(27,14,'Manager','b\'$2b$12$w/1wqceswzUBi5coENhcGuIK/Mn3rNQ0bNhlJoqOD0LG4p9A8rWvu\'',1,'b\'$2b$12$w/1wqceswzUBi5coENhcGu\''),(28,14,'Staff','b\'$2b$12$C/rrYkPOwOCGreleGco/We6YaXVP161H0993DCvRLW15n7VAmMvLK\'',2,'b\'$2b$12$C/rrYkPOwOCGreleGco/We\'');
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

-- Dump completed on 2024-01-04 15:57:11
