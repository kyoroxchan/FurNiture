-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2023-11-29 17:20:15
-- サーバのバージョン： 10.4.28-MariaDB
-- PHP のバージョン: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `furniture`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `admin`
--

CREATE TABLE `admin` (
  `id` varchar(12) NOT NULL,
  `pass` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `admin`
--

INSERT INTO `admin` (`id`, `pass`) VALUES
('123456', 'admin');

-- --------------------------------------------------------

--
-- テーブルの構造 `goods`
--

CREATE TABLE `goods` (
  `gid` int(6) NOT NULL,
  `name` varchar(30) NOT NULL,
  `photo` varchar(100) NOT NULL DEFAULT 'unknownGoods.jpeg',
  `price` int(9) NOT NULL,
  `info` varchar(200) NOT NULL,
  `category` varchar(10) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `sale` varchar(10) NOT NULL DEFAULT 'ok'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `goods`
--

INSERT INTO `goods` (`gid`, `name`, `photo`, `price`, `info`, `category`, `mail`, `sale`) VALUES
(1, '土', '20231129_214859_t-019.jpg', 5200, '土だお。ほんとだお。', 'material', 'test@gmail.com', 'ok'),
(2, '大木', '20231129_220436_992ad18c6c7689112ad0ec2dfe3ec4c0.jpg', 24000, 'とっても大きな木だお。ほんとだお。', 'material', 'test@gmail.com', 'ok'),
(3, '石たち', '20231129_223703_Stone_IMAG1030.jpg', 2499, 'たくさんの石だお。ほんとだお。', 'material', 'test@gmail.com', 'ok'),
(4, 'T字工具', '20231129_224051_TIsq2flmE7gY.jpg', 5600, 'T字の工具です', 'tools', 'test2@gmail.com', 'ok'),
(5, 'ニッパーとか', '20231129_224123_i-img1175x1200-169771867993804oip2.jpg', 1200, 'ニッパーなどのセット売りです', 'tools', 'test2@gmail.com', 'ok'),
(6, '金槌', '20231129_224210_m72254433595_1.jpg', 980, '普通の金槌です', 'tools', 'test2@gmail.com', 'ok'),
(7, 'グルーガン', '20231129_224250_i-img1200x1200-1693202387636lc60di.jpg', 820, 'グルーガンです。グルー四本つけます', 'tools', 'test2@gmail.com', 'ok'),
(8, 'おソファーですわぁ！！', '20231129_224630_MicrosoftTeams-image.png', 0, 'ただですわぁ！！', 'chair', 'test3@gmail.com', 'ok'),
(9, 'おシャンデリアですわぁ！！', '20231129_224704_MicrosoftTeams-image_1.png', 0, 'ただですわぁ！！', 'other', 'test3@gmail.com', 'ok'),
(10, 'お家ですわぁ！！', '20231129_224735_i-img1106x1200-1694088484664qaynvb.jpg', 0, 'ただですわぁ！！', 'other', 'test3@gmail.com', 'ok'),
(11, 'Pig Table', '20231129_225658_201901231747232409.jpg', 569999, 'おとぎ話の召使いのように配膳を行うブタのテーブルです。', 'table', 'test4@gmail.com', 'ok'),
(12, 'Rabbit Lamp', '20231129_225812_jpg65613e22e9a15_EC-15160.jpg', 129999, 'ウサギを忠実に再現したテーブルランプ', 'other', 'test4@gmail.com', 'ok'),
(13, 'Horse Lamp', '20231129_230043_jpg649948d48d917_EC-14771.jpg', 1059999, '馬のリアルなスケール感を忠実に表現した照明', 'other', 'test4@gmail.com', 'ok'),
(14, '青い椅子', '20231129_230733_i-img1200x1200-1699952661121fhyj33.jpg', 8500, '青い椅子です。特徴は青いことです', 'chair', 'takashi@gmail.com', 'ok'),
(15, '青い座椅子', '20231129_230842_i-img900x1200-1699173416958v0w28r.jpg', 4599, '青い座椅子です。特徴は青いことです', 'chair', 'takashi@gmail.com', 'ok'),
(16, 'オレンジの椅子', '20231129_230943_i-img783x992-1701057404ccbvtb7.jpg', 2499, 'オレンジの椅子です。特徴はオレンジが使われていることです', 'chair', 'takashi@gmail.com', 'ok'),
(17, '古い椅子', '20231129_231035_i-img900x1200-1700994789617ryw834.jpg', 12599, '古い椅子です。歴史を感じます', 'chair', 'takashi@gmail.com', 'ok'),
(18, '木の机', '20231129_231133_i-img1200x1200-170090088173344807u_1.jpg', 3450, 'よくある机です。特徴は四つ足なことです', 'table', 'takashi@gmail.com', 'ok'),
(19, '勉強机', '20231129_231220_i-img1200x1200-1696755215189d095ku.jpg', 14500, '勉強机です。特徴は勉強に使える事です', 'table', 'takashi@gmail.com', 'ok'),
(20, '厚い机', '20231129_231312_i-img1200x841-1685275638gll9nl117344.jpg', 1599, '厚い机です。特徴は高さが低いことです', 'table', 'takashi@gmail.com', 'ok'),
(21, '丸い机', '20231129_231404_m53728870480_1.jpg', 7100, '丸い机です。特徴は複数人で使いやすことです', 'table', 'takashi@gmail.com', 'ok'),
(22, '木の板', '20231129_231557_7152OBre3EL._AC_UF8941000_QL80_.jpg', 999, '木の板です。特徴は色々なことに使えることです', 'material', 'takashi@gmail.com', 'ok'),
(23, 'アンパンマンの椅子', '20231129_231701_C7730621.jpg', 3200, 'アンパンマンの椅子です。特徴は子供向けなことです', 'chair', 'takashi@gmail.com', 'ok'),
(24, '猫の置物', '20231129_231822_61t87wgZBHLACSL1500.jpg', 580, '猫の置物です。特徴は宇宙服を着ていることです', 'other', 'takashi@gmail.com', 'ok'),
(25, 'ニッパーandペンチ', '20231129_231924_m72929240621_1.jpg', 220, 'ニッパーとペンチです。特徴はミニサイズなことです', 'tools', 'takashi@gmail.com', 'ok');

-- --------------------------------------------------------

--
-- テーブルの構造 `masaru`
--

CREATE TABLE `masaru` (
  `mid` int(1) NOT NULL,
  `money` int(21) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `masaru`
--

INSERT INTO `masaru` (`mid`, `money`) VALUES
(1, 0);

-- --------------------------------------------------------

--
-- テーブルの構造 `news`
--

CREATE TABLE `news` (
  `nid` int(6) NOT NULL,
  `title` varchar(20) NOT NULL,
  `data` varchar(100) NOT NULL,
  `day` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `news`
--

INSERT INTO `news` (`nid`, `title`, `data`, `day`) VALUES
(1, 'FurNiture', 'FurNitureサイトオープン', '2023-11-29');

-- --------------------------------------------------------

--
-- テーブルの構造 `prepaid`
--

CREATE TABLE `prepaid` (
  `code` varchar(9) NOT NULL,
  `money` int(11) NOT NULL DEFAULT 0,
  `usable` varchar(12) NOT NULL DEFAULT 'ok',
  `issueday` date NOT NULL,
  `useday` date NOT NULL,
  `mail` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `prepaid`
--

INSERT INTO `prepaid` (`code`, `money`, `usable`, `issueday`, `useday`, `mail`) VALUES
('BWH1KVA15', 2000, 'ok', '2023-11-30', '0000-00-00', 'takashi@gmail.com');

-- --------------------------------------------------------

--
-- テーブルの構造 `user`
--

CREATE TABLE `user` (
  `id` int(6) NOT NULL,
  `mail` varchar(40) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `nick` varchar(20) NOT NULL,
  `mei` varchar(6) NOT NULL,
  `mei2` varchar(12) NOT NULL,
  `sei` varchar(6) NOT NULL,
  `sei2` varchar(12) NOT NULL,
  `post` int(7) NOT NULL,
  `pref` varchar(4) NOT NULL,
  `addr` varchar(50) NOT NULL,
  `home` varchar(10) NOT NULL,
  `bname` varchar(50) NOT NULL,
  `phone` int(11) NOT NULL,
  `sex` varchar(10) NOT NULL,
  `news` varchar(10) NOT NULL,
  `icon` varchar(100) NOT NULL DEFAULT 'unknownUser.jpg',
  `profile` varchar(100) NOT NULL,
  `money` int(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `user`
--

INSERT INTO `user` (`id`, `mail`, `pass`, `nick`, `mei`, `mei2`, `sei`, `sei2`, `post`, `pref`, `addr`, `home`, `bname`, `phone`, `sex`, `news`, `icon`, `profile`, `money`) VALUES
(1, 'test@gmail.com', 'test', 'ケビン', '権左衛門', 'ゴンザエモン', '岩井', 'イワイ', 831519, '熊本県', '熊本市', '21-51', '山奥のお家', 2147483647, '男', '受け取らない', '20231129_214324_4466151751_f0df205cb5_o.jpg', 'ケビンだお。ほんとだお。', 10000),
(2, 'test2@gmail.com', 'test', '齋藤', '最中', 'モナカ', '伊藤', 'イトウ', 9891212, '東京都', '銀座', '92-122', '都会すぎるタワー', 2147483647, '男', '受け取らない', '20231129_224020_alphard_pc_1.jpg', '適当に工具売ります', 0),
(3, 'test3@gmail.com', 'test', '壱百満天原サロメ', '押売', 'オシウリ', '只野', 'タダノ', 2141245, '広島県', '広島市', '35-37', '在庫倉庫', 2147483647, '女', '受け取らない', '20231129_224548_NlPBD2mQ_400x400.jpg', '育ちは一般家庭ですわ。', 0),
(4, 'test4@gmail.com', 'test', '鹿鳴館キリコ', '乙女', 'オトメ', '早乙女', 'サオトメ', 2141264, '北海道', '横浜市', '123-456', '別荘', 2147483647, '女', '受け取る', '20231129_225900_keia.jpeg', 'ご機嫌ヨークシャテリア', 0),
(5, 'takashi@gmail.com', 'test', 'たかし(42)', '征十郎', 'セイジュウロウ', '中村', 'ナカムラ', 7881782, '北海道', '十勝', '1-1', 'あの建物', 2147483647, '男', '受け取らない', '20231129_230639_c91739359c8c9e29e6bb2da5c4fbc6ba_t.jpeg', '出品メインでやっていきます', 110000);

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `goods`
--
ALTER TABLE `goods`
  ADD PRIMARY KEY (`gid`);

--
-- テーブルのインデックス `masaru`
--
ALTER TABLE `masaru`
  ADD PRIMARY KEY (`mid`);

--
-- テーブルのインデックス `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`nid`);

--
-- テーブルのインデックス `prepaid`
--
ALTER TABLE `prepaid`
  ADD PRIMARY KEY (`code`);

--
-- テーブルのインデックス `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`,`mail`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `goods`
--
ALTER TABLE `goods`
  MODIFY `gid` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- テーブルの AUTO_INCREMENT `masaru`
--
ALTER TABLE `masaru`
  MODIFY `mid` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- テーブルの AUTO_INCREMENT `news`
--
ALTER TABLE `news`
  MODIFY `nid` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- テーブルの AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
