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
-- Table structure for table `menudishes`
--

DROP TABLE IF EXISTS `menudishes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menudishes` (
  `dishId` int NOT NULL AUTO_INCREMENT,
  `dishName` varchar(45) DEFAULT NULL,
  `menuId` int NOT NULL,
  `price` varchar(45) DEFAULT NULL,
  `timeToCook` int DEFAULT NULL,
  PRIMARY KEY (`dishId`),
  KEY `fk_MenuDishes_Menus1_idx` (`menuId`),
  CONSTRAINT `fk_MenuDishes_Menus1` FOREIGN KEY (`menuId`) REFERENCES `menus` (`menuId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menudishes`
--

LOCK TABLES `menudishes` WRITE;
/*!40000 ALTER TABLE `menudishes` DISABLE KEYS */;
INSERT INTO `menudishes` VALUES (8,'Fillet Steak And Chips',2,'20.54',20),(9,'Spaghetti Bolognese',2,'8.56',13),(10,'Pepperoni Pizza',3,'11.99',15),(11,'Margarita Pizza',3,'10.99',14),(12,'Hawaiian Pizza',3,'11.99',15),(13,'Chocolate Ice Cream',4,'3.45',4);
/*!40000 ALTER TABLE `menudishes` ENABLE KEYS */;
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
