-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2014 年 09 月 18 日 01:51
-- 服务器版本: 5.5.31
-- PHP 版本: 5.4.4-14+deb7u2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `cccms`
--

-- --------------------------------------------------------

--
-- 表的结构 `article`
--

CREATE TABLE IF NOT EXISTS `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `article_class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `article_class_id` (`article_class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `article_class`
--

CREATE TABLE IF NOT EXISTS `article_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_article_class_name` (`name`),
  KEY `parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `category`
--

CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lft` int(11) DEFAULT NULL,
  `rgt` int(11) DEFAULT NULL,
  `layer` int(11) DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_category_title` (`title`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12 ;

--
-- 转存表中的数据 `category`
--

INSERT INTO `category` (`id`, `lft`, `rgt`, `layer`, `title`, `keywords`, `description`, `picture`, `content`, `create_at`, `update_at`) VALUES
(1, 1, 2, 0, 'ROOT', '', '', '', '', '2014-07-29 22:55:47', '2014-07-29 22:55:47'),
(2, 2, 3, 1, '关于我们', '滨州,基督,协会', '', '', '', '2014-07-29 13:04:51', '2014-07-29 13:04:51'),
(3, 4, 11, 1, '新闻中心', '', '', '', '', '2014-07-29 13:05:13', '2014-07-29 13:05:13'),
(4, 5, 8, 2, '企业动态', '', '', '', '', '2014-07-29 13:05:34', '2014-07-29 13:05:34'),
(5, 9, 10, 2, '行业新闻', '', '', '', '', '2014-07-29 13:07:22', '2014-07-29 13:07:22'),
(6, 12, 17, 1, '产品展示', '', '', '', '', '2014-07-29 13:07:42', '2014-07-29 13:07:42'),
(7, 13, 14, 2, '产品分类A', '', '', '', '', '2014-07-29 13:07:59', '2014-07-29 13:07:59'),
(8, 15, 16, 2, '产品分类B', '', '', '', '', '2014-07-29 13:08:15', '2014-07-29 13:08:15'),
(9, 18, 19, 1, '在线留言', '', '', '', '', '2014-07-29 13:08:38', '2014-07-29 13:08:38'),
(10, 20, 21, 1, '联系方式', '', '', '', '', '2014-07-29 13:08:54', '2014-07-29 13:08:54'),
(11, 6, 7, 3, '企业动态01', '', '', '', '', '2014-07-30 04:58:20', '2014-07-30 04:58:20');

-- --------------------------------------------------------

--
-- 表的结构 `config`
--

CREATE TABLE IF NOT EXISTS `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `sitename` varchar(64) DEFAULT NULL,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `domain` varchar(100) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `company_site` varchar(100) DEFAULT NULL,
  `linkman` varchar(100) DEFAULT NULL,
  `tel` varchar(100) DEFAULT NULL,
  `icp` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_config_sitename` (`sitename`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `config`
--

INSERT INTO `config` (`id`, `create_at`, `update_at`, `sitename`, `keywords`, `description`, `domain`, `company`, `company_site`, `linkman`, `tel`, `icp`) VALUES
(1, '2014-07-29 12:23:29', '2014-07-29 12:24:01', '滨州基督教协会', '滨州,基督,协会', '滨州基督教协会', 'www.bzchruch.com', '滨州基督教协会', '', '王国强', '18454350968', '鲁ICP备10086号');

-- --------------------------------------------------------

--
-- 表的结构 `data_model`
--

CREATE TABLE IF NOT EXISTS `data_model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `code` varchar(64) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_data_model_name` (`name`),
  UNIQUE KEY `ix_data_model_code` (`code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- 转存表中的数据 `data_model`
--

INSERT INTO `data_model` (`id`, `name`, `code`, `description`, `is_active`, `create_at`, `update_at`) VALUES
(1, '文章', 'article', '', 0, '2014-07-29 12:14:09', '2014-07-29 12:14:09'),
(2, '产品', 'product', '', 0, '2014-07-29 12:14:24', '2014-07-29 12:14:24'),
(3, '图库', 'picture', '', 0, '2014-07-29 12:15:42', '2014-07-29 12:15:42'),
(4, '单页', 'single_page', '', 0, '2014-07-29 12:16:06', '2014-07-29 12:16:06');

-- --------------------------------------------------------

--
-- 表的结构 `group`
--

CREATE TABLE IF NOT EXISTS `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_group_name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- 转存表中的数据 `group`
--

INSERT INTO `group` (`id`, `create_at`, `update_at`, `name`, `description`) VALUES
(1, '2014-02-21 14:19:14', '2014-02-24 15:13:26', 'test', 'test'),
(2, '2014-02-21 14:19:22', '2014-02-24 15:14:03', 'user', 'user001'),
(3, '2014-02-21 14:19:29', '2014-02-21 14:19:29', 'admin', 'admin'),
(4, '2014-02-21 14:19:45', '2014-02-21 14:19:45', 'superadmin', 'superadmin'),
(5, '2014-03-20 13:18:59', '2014-03-20 13:18:59', '系统管理员', '系统管理员'),
(6, '2014-03-24 23:12:26', '2014-03-24 23:12:26', '普通用户', ''),
(7, '2014-04-23 15:59:43', '2014-04-23 15:59:43', 'test55', '');

-- --------------------------------------------------------

--
-- 表的结构 `member`
--

CREATE TABLE IF NOT EXISTS `member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `member_group_id` int(11) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_member_email` (`email`),
  UNIQUE KEY `ix_member_username` (`username`),
  KEY `member_group_id` (`member_group_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `member`
--

INSERT INTO `member` (`id`, `member_group_id`, `username`, `email`, `password`, `is_active`, `create_at`, `update_at`) VALUES
(1, 1, 'test', 'test999@163.com', 'test999', 1, '2014-07-30 04:33:23', '2014-07-30 04:33:23'),
(2, 1, 'test001', 'test001@cccms.org', 'test001', 1, '2014-07-30 04:33:58', '2014-07-30 04:33:58');

-- --------------------------------------------------------

--
-- 表的结构 `member_group`
--

CREATE TABLE IF NOT EXISTS `member_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_member_group_name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `member_group`
--

INSERT INTO `member_group` (`id`, `name`, `description`, `create_at`, `update_at`) VALUES
(1, '默认会员组', '', '2014-07-29 23:10:55', '2014-07-29 23:10:55'),
(2, 'VIP会员', '', '2014-07-30 04:34:27', '2014-07-30 04:34:27');

-- --------------------------------------------------------

--
-- 表的结构 `picture`
--

CREATE TABLE IF NOT EXISTS `picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `picture_class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `picture_class_id` (`picture_class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `picture_class`
--

CREATE TABLE IF NOT EXISTS `picture_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_picture_class_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `product`
--

CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_class_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_class_id` (`product_class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `product_class`
--

CREATE TABLE IF NOT EXISTS `product_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_product_class_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `product_picture`
--

CREATE TABLE IF NOT EXISTS `product_picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(160) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `posi` int(11) DEFAULT NULL,
  `title` varchar(60) DEFAULT NULL,
  `picture` varchar(60) DEFAULT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_username` (`username`),
  UNIQUE KEY `ix_user_email` (`email`),
  KEY `group_id` (`group_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=20 ;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `create_at`, `update_at`, `group_id`, `username`, `email`, `password`, `is_active`) VALUES
(1, '2014-02-21 14:22:40', '2014-02-24 15:51:04', 2, 'user001', 'user001@test.com', 'user0001', 0),
(2, '2014-02-21 14:23:00', '2014-08-05 22:31:17', 3, 'admin', 'admin@admin8.com', 'admin888', 1),
(3, '2014-02-21 14:23:20', '2014-02-21 14:23:20', 4, 'root', 'root@admin.com', 'test992', 1),
(4, '2014-02-22 14:06:44', '2014-02-22 14:06:44', 1, 'test555', 'test555@test.com', 'test555', 1),
(5, '2014-02-22 14:07:14', '2014-03-26 14:18:05', 1, 'test666', 'test666@test.com', 'test666', 1),
(6, '2014-02-22 14:07:29', '2014-02-22 14:07:29', 1, 'test6665', 'test7@test.com', 'tst555543', 1),
(7, '2014-02-24 15:44:33', '2014-02-24 15:44:33', 1, 'test', 'test', 'test', 1),
(9, '2014-02-24 15:45:10', '2014-02-24 15:45:10', 1, 'test55565', 'test55555@test.com', 'test3323', 1),
(10, '2014-02-24 15:45:28', '2014-02-24 15:45:28', 1, 'test001', 'test001@test.com', 'test888', 1),
(11, '2014-02-24 15:45:49', '2014-02-24 15:45:49', 1, 'test002', 'test001@test.com.cn', 'test', 1),
(12, '2014-02-24 15:46:09', '2014-02-24 15:46:09', 1, 'test556', 'test123@test.com', 'test099', 1),
(13, '2014-02-24 15:51:32', '2014-02-24 15:51:32', 1, 'test222111', 'testst@test002.com', 'test555', 1),
(15, '2014-03-25 22:29:39', '2014-03-25 22:29:39', 1, 'ttetsest001', 'test@test0071.com', 'tets', 1),
(16, '2014-03-25 22:30:10', '2014-03-25 22:38:51', 1, 'admin007', 'admin007@test.com', 'test222', 1),
(17, '2014-03-28 23:40:08', '2014-03-28 23:40:08', 1, 'admin221', 'admin@admin.com', 'admin', 1),
(18, '2014-03-28 23:40:42', '2014-03-29 13:59:42', 1, 'root123', 'root123@admin.com', 'root123', 1),
(19, '2014-03-31 16:22:03', '2014-03-31 16:22:03', 1, 'test5555', 'test5542', 'test', 1);

--
-- 限制导出的表
--

--
-- 限制表 `article`
--
ALTER TABLE `article`
  ADD CONSTRAINT `article_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `article_ibfk_2` FOREIGN KEY (`article_class_id`) REFERENCES `article_class` (`id`);

--
-- 限制表 `article_class`
--
ALTER TABLE `article_class`
  ADD CONSTRAINT `article_class_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `article_class` (`id`);

--
-- 限制表 `member`
--
ALTER TABLE `member`
  ADD CONSTRAINT `member_ibfk_1` FOREIGN KEY (`member_group_id`) REFERENCES `member_group` (`id`);

--
-- 限制表 `picture`
--
ALTER TABLE `picture`
  ADD CONSTRAINT `picture_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `picture_ibfk_2` FOREIGN KEY (`picture_class_id`) REFERENCES `picture_class` (`id`);

--
-- 限制表 `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `product_ibfk_2` FOREIGN KEY (`product_class_id`) REFERENCES `product_class` (`id`);

--
-- 限制表 `product_picture`
--
ALTER TABLE `product_picture`
  ADD CONSTRAINT `product_picture_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `product_picture_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- 限制表 `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
