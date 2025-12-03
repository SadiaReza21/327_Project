-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 03, 2025 at 10:45 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bazarkori_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `archived`
--

CREATE TABLE `archived` (
  `product_id` bigint(20) NOT NULL,
  `stock` int(10) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `is_archived` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `archived`
--

INSERT INTO `archived` (`product_id`, `stock`, `name`, `is_archived`) VALUES
(124, 0, 'Cucumber', 1),
(1763982157625, 0, NULL, 1),
(1764007134677, 0, NULL, 1),
(1764327326412, 0, NULL, 1),
(1764514616278, 0, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`) VALUES
(1, 'Fruits & Vegetables'),
(2, 'Meat & Fish'),
(3, 'Dairy & Eggs'),
(4, 'Bakery'),
(5, 'Pantry Staples & Groceries'),
(6, 'Cooking Essentials'),
(7, 'Rice, Pasta & Noodles'),
(8, 'Canned & Jarred Foods'),
(9, 'Breakfast & Cereals'),
(10, 'Beverages'),
(11, 'Soft Drinks & Juices'),
(12, 'Hot Drinks'),
(14, 'Frozen & Chilled Foods'),
(15, 'Frozen Meals & Snacks'),
(16, 'Chilled Items'),
(17, 'Household Essentials'),
(18, 'Cleaning Supplies'),
(19, 'Home & Kitchen'),
(20, 'Personal Care & Health'),
(21, 'Health & Wellness'),
(22, 'Beauty & Personal Care'),
(23, 'Other'),
(24, 'Baby Care'),
(25, 'Pet Supplies'),
(26, 'Snacks & Confectionery');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` bigint(20) NOT NULL,
  `category_id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL,
  `description` text DEFAULT NULL,
  `price` double NOT NULL,
  `stock` int(10) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `date_added` date NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `is_archived` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `category_id`, `name`, `description`, `price`, `stock`, `image_url`, `date_added`, `is_available`, `is_archived`) VALUES
(124, 5, 'Cucumber', 'Absolutely fresh 40 gm cucumber', 45.5, 0, 'ProductImages/124/124.jpg', '2025-12-03', 1, 1),
(1763982157625, 1, 'Milk - 10 litre', 'jhj', 50.3, 5, 'ProductImages/1763982157625/1763982157625.png', '2025-11-28', 1, 1),
(1764007134677, 2, 'Katla 800gm', 'Fresh from river', 1200, 0, 'ProductImages/default.png', '2025-11-30', 1, 1),
(1764313211541, 11, 'Onion - 100gm', 'Fresh from Farm', 60, 50, 'ProductImages/default.png', '2025-11-28', 1, 0),
(1764327326412, 6, 'gffg', '', 343, 5, 'ProductImages/default.png', '2025-11-28', 1, 1),
(1764514616278, 18, 'LalShak - 200gm', 'dgfgdfbfd ddsfd dfgfdgfdg dgdfgfgf fgfdgfdg ffgfgf dgfdgfgfg dfgffg', 70, 34, 'ProductImages/1764514616278/1764514616278.png', '2025-11-30', 1, 1),
(1764739292201, 25, 'Potato - 500gm', 'dfdsfdfs', 70, 4545, 'ProductImages/1764739292201/1764739292201.webp', '2025-12-03', 1, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `archived`
--
ALTER TABLE `archived`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `category_id` (`category_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `archived`
--
ALTER TABLE `archived`
  ADD CONSTRAINT `archived_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
