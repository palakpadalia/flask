-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 19, 2022 at 05:09 PM
-- Server version: 10.6.7-MariaDB-2ubuntu1
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(255) NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(2, 'palakpadalia19@gmail.com', 'b81618b6fda05785c56b9eddfb8862d8');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(255) NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `user_name`, `password`) VALUES
(1, 'foramshah@gmail.com', 'foramshah', '7f2593e8a4e6ea5f9862fd58fc81a4a1'),
(3, 'palakpadalia19@gmail.com', 'palak', 'b81618b6fda05785c56b9eddfb8862d8'),
(5, 'xomu@mailinator.com', 'hamikole', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(6, 'vufyjogy@mailinator.com', 'jetiq', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(7, 'piquqir@mailinator.com', 'paduj', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(9, 'juhocyzu@mailinator.com', 'xyfysorityuukij', 'b81618b6fda05785c56b9eddfb8862d8'),
(10, 'lozaqu@mailinator.com', 'visybuju', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(11, 'xywupepyvo@mailinator.com', 'hociwum', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(12, 'qehokumej@mailinator.com', 'qifoz', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(14, 'lyxi@mailinator.com', 'ganupuio', '95fc913122d33902041da966a43c78b9'),
(15, 'rusewan@mailinator.com', 'dibeqim', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(16, 'ruco@mailinator.com', 'dyvizohese', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(17, 'qigaci@mailinator.com', 'fekyz', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(18, 'jyzucopa@mailinator.com', 'woruq', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(19, 'sidiwoqo@mailinator.com', 'jenelypiva', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(21, 'habyqig@mailinator.com', 'havotu', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(22, 'mafa@mailinator.com', 'rybuqo', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(23, 'regejanibi@mailinator.com', 'bidopud', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(24, 'pyniz@mailinator.com', 'qevixagaku', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(25, 'sifidivyry@mailinator.com', 'kyxohi', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(26, 'nutex@mailinator.com', 'fugygaxaco', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(27, 'loxyhixymu@mailinator.com', 'fopixym', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(28, 'gahu@mailinator.com', 'tuqiw', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(29, 'woximu@mailinator.com', 'zubifeni', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(30, 'nijytihuh@mailinator.com', 'pycopykyjy', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(31, 'guten@mailinator.com', 'nezuha', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(32, 'xojop@mailinator.com', 'wenosejy', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(33, 'juninoxamy@mailinator.com', 'gazesonyl', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(37, 'giqyricis@mailinator.com', 'cafixas', 'f3ed11bbdb94fd9ebdefbaf646ab94d3'),
(38, 'lole@mailinator.com', 'paliseriwe', 'f3ed11bbdb94fd9ebdefbaf646ab94d3');

-- --------------------------------------------------------

--
-- Table structure for table `user_profile`
--

CREATE TABLE `user_profile` (
  `id` int(255) NOT NULL,
  `user_id` int(50) NOT NULL,
  `first_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date NOT NULL,
  `dobc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mobile_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `state` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `zipcode` int(10) NOT NULL,
  `image` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profile_updated_dt` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `user_profile`
--

INSERT INTO `user_profile` (`id`, `user_id`, `first_name`, `last_name`, `date_of_birth`, `dobc`, `mobile_number`, `gender`, `address`, `city`, `state`, `zipcode`, `image`, `profile_updated_dt`) VALUES
(1, 1, 'foram', 'Shah', '2003-12-25', 'Assignment.pdf', '9746789067', 'Female', 'moti baug near kalva chowk', 'Ahemdabad', 'Andhra Pradesh', 855689, 'sample1.jpeg', '2022-07-19');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `user_name` (`user_name`);

--
-- Indexes for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `user_profile`
--
ALTER TABLE `user_profile`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD CONSTRAINT `user_profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
