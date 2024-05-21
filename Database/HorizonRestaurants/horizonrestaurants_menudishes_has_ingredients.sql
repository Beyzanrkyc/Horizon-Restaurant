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
-- Table structure for table `menudishes_has_ingredients`
--

DROP TABLE IF EXISTS `menudishes_has_ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menudishes_has_ingredients` (
  `dishId` int NOT NULL,
  `itemId` int NOT NULL,
  PRIMARY KEY (`dishId`,`itemId`),
  KEY `fk_MenuDishes_has_Ingredients_Ingredients1_idx` (`itemId`),
  KEY `fk_MenuDishes_has_Ingredients_MenuDishes1_idx` (`dishId`),
  CONSTRAINT `fk_MenuDishes_has_Ingredients_Ingredients1` FOREIGN KEY (`itemId`) REFERENCES `ingredients` (`itemId`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_MenuDishes_has_Ingredients_MenuDishes1` FOREIGN KEY (`dishId`) REFERENCES `menudishes` (`dishId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menudishes_has_ingredients`
--

LOCK TABLES `menudishes_has_ingredients` WRITE;
/*!40000 ALTER TABLE `menudishes_has_ingredients` DISABLE KEYS */;
INSERT INTO `menudishes_has_ingredients` VALUES (8,1),(8,2),(9,3),(9,4),(10,5),(11,5),(12,5),(10,6),(11,6),(12,6),(10,7),(11,7),(10,8),(12,9),(12,10),(13,11),(13,12);
/*!40000 ALTER TABLE `menudishes_has_ingredients` ENABLE KEYS */;
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
