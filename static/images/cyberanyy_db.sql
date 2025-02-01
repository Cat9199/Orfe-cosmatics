-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 01, 2025 at 11:35 AM
-- Server version: 8.0.41-0ubuntu0.22.04.1
-- PHP Version: 8.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cyberanyy_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bootcamps`
--

CREATE TABLE `bootcamps` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category_id` bigint UNSIGNED NOT NULL,
  `price` double NOT NULL,
  `bootcamp_date` date NOT NULL,
  `duration` int NOT NULL,
  `workshops` int DEFAULT NULL,
  `projects` int DEFAULT NULL,
  `missions` int DEFAULT NULL,
  `weeks` int DEFAULT NULL,
  `effect` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `language` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sponsored` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bootcamps`
--

INSERT INTO `bootcamps` (`id`, `name`, `image`, `category_id`, `price`, `bootcamp_date`, `duration`, `workshops`, `projects`, `missions`, `weeks`, `effect`, `language`, `sponsored`, `created_at`, `updated_at`) VALUES
(1, 'بوت كام البرمجه من الصفر', '01JDPWV8S4QMMXPW92G0GFE9RH.jpg', 1, 50, '2024-11-15', 20, 20, 33, 30, 33, 'قابل للتوظيف', 'عربي', 1, '2024-11-15 14:52:28', '2024-11-27 13:26:53'),
(2, 'Haviva Wallace', '01JDYFPSQZGJZZNEGBQEVYJJSX.jpg', 2, 829, '2002-10-16', 64, 48, 95, 14, 69, 'Ex quia laborum Sint molestiae placeat enim optio et expedita maxime rerum irure amet est', 'Id magnam labore reprehenderit eos lorem officiis consectetur', 1, '2024-11-30 12:11:10', '2024-11-30 12:11:10');

-- --------------------------------------------------------

--
-- Table structure for table `bootcamp_course`
--

CREATE TABLE `bootcamp_course` (
  `id` bigint UNSIGNED NOT NULL,
  `bootcamp_id` bigint UNSIGNED NOT NULL,
  `course_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bootcamp_course`
--

INSERT INTO `bootcamp_course` (`id`, `bootcamp_id`, `course_id`) VALUES
(1, 1, 1),
(2, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `bootcamp_features`
--

CREATE TABLE `bootcamp_features` (
  `id` bigint UNSIGNED NOT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bootcamp_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bootcamp_features`
--

INSERT INTO `bootcamp_features` (`id`, `value`, `bootcamp_id`, `created_at`, `updated_at`) VALUES
(1, 'المميزا1', 1, '2024-11-15 14:52:28', '2024-11-15 14:52:28'),
(2, 'المميزا2', 1, '2024-11-15 14:52:28', '2024-11-15 14:52:28'),
(3, 'المميزا3', 1, '2024-11-15 14:52:28', '2024-11-15 14:52:28'),
(4, 'Est sed aut facere commodo ut cum lorem dolores pariatur Consequatur mollitia', 2, '2024-11-30 12:11:10', '2024-11-30 12:11:10');

-- --------------------------------------------------------

--
-- Table structure for table `bootcamp_requirements`
--

CREATE TABLE `bootcamp_requirements` (
  `id` bigint UNSIGNED NOT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bootcamp_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bootcamp_requirements`
--

INSERT INTO `bootcamp_requirements` (`id`, `value`, `bootcamp_id`, `created_at`, `updated_at`) VALUES
(1, 'شلشسل', 1, '2024-11-15 14:52:28', '2024-11-15 14:52:28'),
(2, 'شسلشسل', 1, '2024-11-15 14:52:28', '2024-11-15 14:52:28'),
(3, 'شسلشسل', 1, '2024-11-15 14:52:28', '2024-11-15 14:52:28'),
(4, 'شسلشسل', 1, '2024-11-15 14:52:28', '2024-11-15 14:52:28'),
(5, 'Consequatur sit qui aliquam magna hic dolore enim nesciunt soluta', 2, '2024-11-30 12:11:10', '2024-11-30 12:11:10');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, 'برمجه', '2024-11-15 14:47:00', '2024-11-15 14:47:00'),
(2, 'تصميم', '2024-11-15 14:47:03', '2024-11-15 14:47:03'),
(3, 'DevOps', '2024-11-15 14:47:20', '2024-11-15 14:47:20');

-- --------------------------------------------------------

--
-- Table structure for table `chapters`
--

CREATE TABLE `chapters` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration` int NOT NULL,
  `course_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `chapters`
--

INSERT INTO `chapters` (`id`, `title`, `duration`, `course_id`, `created_at`, `updated_at`) VALUES
(1, 'شابتر 1', 50, 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54');

-- --------------------------------------------------------

--
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `contact_messages`
--

INSERT INTO `contact_messages` (`id`, `name`, `mobile`, `email`, `message`, `created_at`, `updated_at`) VALUES
(1, 'MacKensie Jenkins', 'Sed nulla ut soluta', 'vufor@mailinator.com', 'Beatae et dolorum fu', '2024-11-19 10:33:11', '2024-11-19 10:33:11'),
(2, 'JNROkufF', 'JNROku', 'JNROkufF@burpcollaborator.net', '\'D13\'DG \'D.\'5 (C', '2025-01-07 12:53:14', '2025-01-07 12:53:14'),
(3, 'JNROkufF', 'JNROku', 'JNROkufF@burpcollaborator.net', '\'D13\'DG \'D.\'5 (C', '2025-01-07 12:54:52', '2025-01-07 12:54:52');

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category_id` bigint UNSIGNED NOT NULL,
  `course_date` date NOT NULL,
  `price` double NOT NULL,
  `duration` int NOT NULL,
  `workshops` int DEFAULT NULL,
  `missions` int DEFAULT NULL,
  `projects` int DEFAULT NULL,
  `weeks` int DEFAULT NULL,
  `effect` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `language` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `name`, `image`, `category_id`, `course_date`, `price`, `duration`, `workshops`, `missions`, `projects`, `weeks`, `effect`, `language`, `created_at`, `updated_at`) VALUES
(1, 'كورس برمجه الفرونت اند من الصفر', '01JDPWT587ANK63MNWM41G1HTQ.jpg', 1, '2024-11-15', 50, 20, 25, 55, 55, 55, 'توظيف', 'عربي', '2024-11-15 14:50:54', '2024-11-27 13:26:17');

-- --------------------------------------------------------

--
-- Table structure for table `course_features`
--

CREATE TABLE `course_features` (
  `id` bigint UNSIGNED NOT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `course_features`
--

INSERT INTO `course_features` (`id`, `value`, `course_id`, `created_at`, `updated_at`) VALUES
(1, 'ميزه رقم 1', 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54'),
(2, 'ميزه رقم 1', 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54'),
(3, 'ميزه رقم 1', 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54');

-- --------------------------------------------------------

--
-- Table structure for table `course_requirements`
--

CREATE TABLE `course_requirements` (
  `id` bigint UNSIGNED NOT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `course_requirements`
--

INSERT INTO `course_requirements` (`id`, `value`, `course_id`, `created_at`, `updated_at`) VALUES
(1, 'المتطلبات 1', 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54'),
(2, 'المتطلبات 1', 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54'),
(3, 'المتطلبات 1', 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54');

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint UNSIGNED NOT NULL,
  `uuid` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `connection` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `queue` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `payload` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `exception` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `faqs`
--

CREATE TABLE `faqs` (
  `id` bigint UNSIGNED NOT NULL,
  `question` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `faqs`
--

INSERT INTO `faqs` (`id`, `question`, `answer`, `created_at`, `updated_at`) VALUES
(1, 'asgasg', 'asgsagasg', '2024-11-19 09:13:12', '2024-11-19 09:13:12');

-- --------------------------------------------------------

--
-- Table structure for table `lessons`
--

CREATE TABLE `lessons` (
  `id` bigint UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` enum('Meeting','Video','Discussion','Exam') COLLATE utf8mb4_unicode_ci NOT NULL,
  `chapter_id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `lessons`
--

INSERT INTO `lessons` (`id`, `title`, `type`, `chapter_id`, `created_at`, `updated_at`) VALUES
(1, 'كورس برمجه', 'Meeting', 1, '2024-11-15 14:50:54', '2024-11-15 14:50:54'),
(2, 'بشسبشسب', 'Video', 1, '2024-11-15 14:50:54', '2024-11-27 13:26:27');

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int UNSIGNED NOT NULL,
  `migration` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `batch` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '2014_10_12_000000_create_users_table', 1),
(2, '2014_10_12_100000_create_password_reset_tokens_table', 1),
(3, '2019_08_19_000000_create_failed_jobs_table', 1),
(4, '2019_12_14_000001_create_personal_access_tokens_table', 1),
(5, '2024_05_14_200434_create_contact_messages_table', 1),
(6, '2024_05_14_200446_create_categories_table', 1),
(7, '2024_06_05_183358_create_courses_table', 1),
(8, '2024_06_05_183427_create_chapters_table', 1),
(9, '2024_06_05_183433_create_lessons_table', 1),
(10, '2024_06_05_183455_create_payment_methods_table', 1),
(11, '2024_06_05_183501_create_bootcamps_table', 1),
(12, '2024_06_05_183525_create_bootcamp_course_table', 1),
(13, '2024_06_05_191829_create_course_features_table', 1),
(14, '2024_06_05_191835_create_course_requirements_table', 1),
(15, '2024_06_05_191842_create_bootcamp_features_table', 1),
(16, '2024_06_05_191850_create_bootcamp_requirements_table', 1),
(17, '2024_06_05_192203_create_user_favorites_table', 1),
(18, '2024_06_05_192459_create_faqs_table', 1),
(19, '2024_06_06_132145_add_sponsored_boolean_to_bootcamps_table', 1),
(20, '2024_06_06_133423_create_reviews_table', 1),
(21, '2024_06_06_141543_create_reservations_table', 1);

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payment_methods`
--

CREATE TABLE `payment_methods` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `payment_methods`
--

INSERT INTO `payment_methods` (`id`, `name`, `value`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Instapay', '011111111111', 1, '2024-11-23 14:56:23', '2024-11-23 14:56:23'),
(2, 'Vodafone Cash', '011111111111', 1, '2024-11-23 14:56:37', '2024-11-23 14:56:37'),
(3, 'Paymob', '011111111111', 1, '2024-11-23 14:56:55', '2024-11-23 14:56:55');

-- --------------------------------------------------------

--
-- Table structure for table `personal_access_tokens`
--

CREATE TABLE `personal_access_tokens` (
  `id` bigint UNSIGNED NOT NULL,
  `tokenable_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tokenable_id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `token` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `abilities` text COLLATE utf8mb4_unicode_ci,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `personal_access_tokens`
--

INSERT INTO `personal_access_tokens` (`id`, `tokenable_type`, `tokenable_id`, `name`, `token`, `abilities`, `last_used_at`, `expires_at`, `created_at`, `updated_at`) VALUES
(1, 'App\\Models\\User', 2, 'auth-token', 'ca027e27c2885c197ce2a00a952587a9bff48ff969514f7395e916985ba2f355', '[\"*\"]', '2024-12-01 13:43:43', NULL, '2024-11-19 10:57:22', '2024-12-01 13:43:43'),
(2, 'App\\Models\\User', 3, 'auth-token', '9d2fa7d86a11c06c119ab0089f46f586414942520161734f6eacede33420f5b4', '[\"*\"]', '2024-12-01 14:05:05', NULL, '2024-11-19 12:11:33', '2024-12-01 14:05:05'),
(3, 'App\\Models\\User', 4, 'auth-token', '01ea0c50a4332bdbab268232476238e0192dedfc720c53c2071afad4372cbabb', '[\"*\"]', '2024-11-29 11:37:03', NULL, '2024-11-23 12:52:46', '2024-11-29 11:37:03'),
(4, 'App\\Models\\User', 6, 'auth-token', '57f17c6eb08b45d13856dca623b9d52fc813f8f99cf78222372ee320df83617c', '[\"*\"]', '2025-01-06 12:10:39', NULL, '2025-01-06 12:07:00', '2025-01-06 12:10:39'),
(5, 'App\\Models\\User', 8, 'auth-token', 'eebfecaf8db023f213eaaf98f8fef8982f01dc5400cab3b062758bfd7eefb294', '[\"*\"]', NULL, NULL, '2025-01-07 11:14:54', '2025-01-07 11:14:54'),
(6, 'App\\Models\\User', 9, 'auth-token', 'e615c61ed2623d5f6ec728250d9e8d53edceb394ecf3769a72bff90d51fba6e3', '[\"*\"]', '2025-01-07 11:15:37', NULL, '2025-01-07 11:15:17', '2025-01-07 11:15:37');

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `id` bigint UNSIGNED NOT NULL,
  `code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `bootcamp_id` bigint UNSIGNED DEFAULT NULL,
  `course_id` bigint UNSIGNED DEFAULT NULL,
  `type` tinyint NOT NULL,
  `payment_price` double DEFAULT NULL,
  `payment_type` tinyint NOT NULL,
  `payment_from_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `reservations`
--

INSERT INTO `reservations` (`id`, `code`, `user_id`, `bootcamp_id`, `course_id`, `type`, `payment_price`, `payment_type`, `payment_from_number`, `payment_image`, `status`, `note`, `details`, `created_at`, `updated_at`) VALUES
(1, '#84885828', 2, 1, NULL, 2, 50, 1, '01454874541', 'reservations/DIAu4BSJXO1hKeb0kqwUcLsm3jZPHmFhTfieRyhA.jpg', 0, 'test', NULL, '2024-11-19 11:01:18', '2024-11-19 11:01:18'),
(2, '#81487847', 2, 1, NULL, 2, 50, 3, '01454874541', 'reservations/LgUayNuB4kBXbTbIdXR8218C7wT01PF7cC5caezf.jpg', 0, 'test', NULL, '2024-11-19 11:01:29', '2024-11-19 11:01:29'),
(3, '#97392726', 3, 1, NULL, 2, 50, 1, '01011653271', 'reservations/1sSgUhlHx7yIwIdbEyK8lZxJLtR6fu6R8dTTTuCF.jpg', 0, 'gasgasgasg', NULL, '2024-11-19 12:12:13', '2024-11-19 12:12:13'),
(4, '#72170583', 2, 1, NULL, 2, 50, 1, '01066625846', 'reservations/1WqQHiEPnMh91btPnTpMyAjSYEfGfVw6PoojRJfw.jpg', 0, NULL, NULL, '2024-11-19 12:21:30', '2024-11-19 12:21:30'),
(5, '#67243035', 3, 1, NULL, 2, 50, 1, '01011653271', 'reservations/kJAfgtgP6toncbu8xJ7oCQHLPoGwZZsqfv5dVNZL.png', 1, 'شسلشسل', NULL, '2024-11-23 12:50:24', '2024-11-26 08:59:49'),
(6, '#15459708', 2, 1, NULL, 2, 50, 1, '01454874541', 'reservations/pZd0l3o96cA8SCKweP5FOkhlHJ1r17PRPeTedY9y.jpg', 1, NULL, NULL, '2024-11-25 16:32:52', '2024-11-26 08:59:19'),
(7, '#54438884', 2, 1, NULL, 2, 50, 1, '01066625846', 'reservations/aooPbAgbdTetPrZ5RVCbY8YcqdB3holKWAfo4ZyP.jpg', 1, NULL, NULL, '2024-11-25 16:37:12', '2024-11-26 08:58:15'),
(8, '#82863566', 2, 1, NULL, 2, 50, 1, '01454874541', 'reservations/mBq4OmWH7v8LqIl2LGAicwY3BOSs2dJL8f60vnkV.jpg', 1, NULL, NULL, '2024-11-30 11:59:56', '2024-11-30 12:10:38'),
(9, '#31436103', 6, 1, NULL, 2, 50, 1, '01011653271', 'reservations/Rk8NA0WJsdQlEi04dPsHAyagdeLxCgUjHvxBNx86.png', 1, 'بشسبشسب', NULL, '2025-01-06 12:07:54', '2025-01-06 12:09:08');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `name`, `image`, `title`, `description`, `created_at`, `updated_at`) VALUES
(1, 'سشيشسي', '01JDPWWPZBWBZZXVG1ZXBXEY21.jpg', 'asfasfasf', 'asgasgsag', '2024-11-19 09:13:01', '2024-11-27 13:27:40');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mobile` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `verification_code` smallint DEFAULT NULL,
  `code_expiration` timestamp NULL DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `role` tinyint NOT NULL DEFAULT '1',
  `remember_token` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `code`, `email`, `mobile`, `email_verified_at`, `verification_code`, `code_expiration`, `password`, `status`, `role`, `remember_token`, `created_at`, `updated_at`) VALUES
(1, 'admin01', NULL, 'USER-44129920', 'admin@admin.com', NULL, '2024-11-18 13:30:48', NULL, NULL, '$2y$10$L4yzx2TAri53rzCHy3cacOd7GYCmin1P7WxqtrCZOPKj5cAKwCmHO', 0, 0, NULL, '2024-11-13 11:14:35', '2024-11-13 11:14:35'),
(2, 'yousef mostafa abas', 'yousef mostafa', 'USER-54199042', 'test@gmail.com', '+201550223079', '2024-11-19 10:57:22', NULL, NULL, '$2y$12$jQ9My6y1XT/TxuJdY.JdjeiCLP8q/VGJETudVYX8CgkFXSiP7eO9.', 1, 1, '1|EcbJM7G91oNbrbrhRQsTTM3GGsvwzngJa3mbQAY8e6251db1', '2024-11-19 10:57:06', '2024-11-30 10:28:41'),
(3, 'gamal', 'rasco', 'USER-75980263', 'xrascoz@gmail.com', '+201011653271', '2024-11-19 12:11:33', NULL, NULL, '$2y$12$1TewgMOh3PtPzD8cI5shbOc3nYMrTOQ4eKEutTjHZ4eeUnWsJTYL2', 1, 1, '2|uqRjQFupV9Aeal6jtzjJcRfId1gbKMQO0zS1ejkN9f376085', '2024-11-19 12:10:51', '2024-11-19 12:11:33'),
(4, 'Youssef', 'youssefdegweyy2', 'USER-52740635', 'youssefeldegwey@gmail.com', '01066625846', '2024-11-23 12:52:46', NULL, NULL, '$2y$12$mzt4.IOaCPT.c1fOx8I3u.IM6vUUzxd7UIuNQ9eXyxU0aPtW4F9f.', 1, 1, '3|aTJQYiBa5mcNa7I3USZ3Ze4fOYgPxpqw93tQMYnp84d1ec1d', '2024-11-23 12:52:39', '2024-11-23 12:53:38'),
(5, 'Mohammed', 'Secfathy', 'USER-48468203', 'secfathy@gmail.com', '+201025576136', NULL, 1111, '2025-01-04 20:24:18', '$2y$12$8Xjyu5BlvMF6os4UnseGwOv9YJPnmGxdFvATAvaFvr.i5rUt4rXS2', 0, 1, NULL, '2025-01-04 19:25:08', '2025-01-04 20:14:18'),
(6, 'vaway76162', 'vaway76162', 'USER-42820916', 'vaway76162@pixdd.com', '+201011653271', '2025-01-06 12:07:00', 1111, '2025-01-06 12:25:58', '$2y$12$UEsJQts9fhs6JqMDqjWl2uVL7wTPq/8vqW/mGqDFfuzbq2pGISyX6', 1, 1, '4|pXZkMDZDLu2cbFlkLazAb83Mdi28Vv1MiV7xYV960904d165', '2025-01-06 12:06:43', '2025-01-06 12:15:58'),
(7, 'abdulhai gamal', 'ficice1932', 'USER-56264384', 'ficice1932@chansd.com', '+201011653271', NULL, 1111, '2025-01-06 12:21:20', '$2y$12$by5idflRMYHs612TBKE.GuM9T3t.BaJSDSvLRhr4O6gfzZU/wld9e', 0, 1, NULL, '2025-01-06 12:11:20', '2025-01-06 12:11:20'),
(8, 'Serina King', 'fofodugego', 'USER-27568614', 'bapesara@mailinator.com', '+201011530060', '2025-01-07 11:14:54', NULL, NULL, '$2y$12$n5mx.v8iz1W.rWWvYi08u.Ajhx/2Bk/vJ5T0PAluZb9FJPWDM0KE.', 1, 1, '5|3kLKbA9eVUCd3o7cBvVnYSzGYHhv0GxySOEXFLeN1d5750cf', '2025-01-07 11:14:50', '2025-01-07 11:14:54'),
(9, 'Jakeem Henson', 'vivif', 'USER-28731378', 'xiguna@mailinator.com', '+441000', '2025-01-07 11:15:17', NULL, NULL, '$2y$12$DMNZYOp8ZipzBVIWoDM4UOwLhKMkZ.3NL6UY5TinRFour9J7wz6My', 1, 1, '6|Do8VISU3hRfLBGoY4Wus3NmoUSwcIQq3lEy9IPYL2d12c312', '2025-01-07 11:15:13', '2025-01-07 11:15:17'),
(10, 'EtjiCoNC', 'EtjiCoNC', 'USER-41214881', 'EtjiCoNC@burpcollaborator.net', '+4841615577', NULL, 1111, '2025-01-07 13:06:47', '$2y$12$jogMRWaeIFZ6k1GModegIunsZPOLTQzu7CrJeFSLwfUGohcinw1RO', 0, 1, NULL, '2025-01-07 12:56:47', '2025-01-07 12:56:47');

-- --------------------------------------------------------

--
-- Table structure for table `user_favorites`
--

CREATE TABLE `user_favorites` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `bootcamp_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `user_favorites`
--

INSERT INTO `user_favorites` (`id`, `user_id`, `bootcamp_id`) VALUES
(3, 3, 1),
(5, 4, 1),
(11, 2, 2),
(12, 6, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bootcamps`
--
ALTER TABLE `bootcamps`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bootcamp_course`
--
ALTER TABLE `bootcamp_course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bootcamp_course_bootcamp_id_foreign` (`bootcamp_id`),
  ADD KEY `bootcamp_course_course_id_foreign` (`course_id`);

--
-- Indexes for table `bootcamp_features`
--
ALTER TABLE `bootcamp_features`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bootcamp_features_bootcamp_id_foreign` (`bootcamp_id`);

--
-- Indexes for table `bootcamp_requirements`
--
ALTER TABLE `bootcamp_requirements`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bootcamp_requirements_bootcamp_id_foreign` (`bootcamp_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chapters`
--
ALTER TABLE `chapters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chapters_course_id_foreign` (`course_id`);

--
-- Indexes for table `contact_messages`
--
ALTER TABLE `contact_messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `course_features`
--
ALTER TABLE `course_features`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_features_course_id_foreign` (`course_id`);

--
-- Indexes for table `course_requirements`
--
ALTER TABLE `course_requirements`
  ADD PRIMARY KEY (`id`),
  ADD KEY `course_requirements_course_id_foreign` (`course_id`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `faqs`
--
ALTER TABLE `faqs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `lessons`
--
ALTER TABLE `lessons`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lessons_chapter_id_foreign` (`chapter_id`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `payment_methods`
--
ALTER TABLE `payment_methods`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  ADD KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`),
  ADD UNIQUE KEY `users_username_unique` (`username`);

--
-- Indexes for table `user_favorites`
--
ALTER TABLE `user_favorites`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_favorites_user_id_foreign` (`user_id`),
  ADD KEY `user_favorites_bootcamp_id_foreign` (`bootcamp_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bootcamps`
--
ALTER TABLE `bootcamps`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bootcamp_course`
--
ALTER TABLE `bootcamp_course`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bootcamp_features`
--
ALTER TABLE `bootcamp_features`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `bootcamp_requirements`
--
ALTER TABLE `bootcamp_requirements`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `chapters`
--
ALTER TABLE `chapters`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `contact_messages`
--
ALTER TABLE `contact_messages`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `course_features`
--
ALTER TABLE `course_features`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `course_requirements`
--
ALTER TABLE `course_requirements`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `faqs`
--
ALTER TABLE `faqs`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `lessons`
--
ALTER TABLE `lessons`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `payment_methods`
--
ALTER TABLE `payment_methods`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user_favorites`
--
ALTER TABLE `user_favorites`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bootcamp_course`
--
ALTER TABLE `bootcamp_course`
  ADD CONSTRAINT `bootcamp_course_bootcamp_id_foreign` FOREIGN KEY (`bootcamp_id`) REFERENCES `bootcamps` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bootcamp_course_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `bootcamp_features`
--
ALTER TABLE `bootcamp_features`
  ADD CONSTRAINT `bootcamp_features_bootcamp_id_foreign` FOREIGN KEY (`bootcamp_id`) REFERENCES `bootcamps` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `bootcamp_requirements`
--
ALTER TABLE `bootcamp_requirements`
  ADD CONSTRAINT `bootcamp_requirements_bootcamp_id_foreign` FOREIGN KEY (`bootcamp_id`) REFERENCES `bootcamps` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `chapters`
--
ALTER TABLE `chapters`
  ADD CONSTRAINT `chapters_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `course_features`
--
ALTER TABLE `course_features`
  ADD CONSTRAINT `course_features_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `course_requirements`
--
ALTER TABLE `course_requirements`
  ADD CONSTRAINT `course_requirements_course_id_foreign` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lessons`
--
ALTER TABLE `lessons`
  ADD CONSTRAINT `lessons_chapter_id_foreign` FOREIGN KEY (`chapter_id`) REFERENCES `chapters` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user_favorites`
--
ALTER TABLE `user_favorites`
  ADD CONSTRAINT `user_favorites_bootcamp_id_foreign` FOREIGN KEY (`bootcamp_id`) REFERENCES `bootcamps` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_favorites_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
