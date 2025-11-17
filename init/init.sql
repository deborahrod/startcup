--
-- Base de Dados: `criptoRace`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `acertoCandidato`
--

CREATE TABLE IF NOT EXISTS `acertoCandidato` (
  `idAcertos` int(11) NOT NULL AUTO_INCREMENT,
  `idDesafio` int(11) DEFAULT NULL,
  `idRespostaSubmetida` int(11) DEFAULT NULL,
  `pontuacao` int(11) NOT NULL,
  PRIMARY KEY (`idAcertos`),
  KEY `fk_acertoCandidato_desafios` (`idDesafio`),
  KEY `fk_acertoCandidato_respostaSubmetida` (`idRespostaSubmetida`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;



-- --------------------------------------------------------

--
-- Estrutura da tabela `candidato`
--

CREATE TABLE IF NOT EXISTS `candidato` (
  `idCandidato` int(11) NOT NULL AUTO_INCREMENT,
  `nomeCompleto` varchar(100) NOT NULL,
  `nick` varchar(100) NOT NULL,
  `matriculaIFG` varchar(30) NOT NULL,
  `chave` varchar(15) NOT NULL,
  `tipo` int(11) NOT NULL,
  PRIMARY KEY (`idCandidato`),
  UNIQUE KEY `matriculaIFG` (`matriculaIFG`),
  UNIQUE KEY `chave` (`chave`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1000 ;


CREATE TABLE IF NOT EXISTS `time` (
  `idTime` INT AUTO_INCREMENT PRIMARY KEY,
  `nomeTime` VARCHAR(100) NOT NULL UNIQUE,
  `lider` INT NOT NULL,
    CONSTRAINT `fk_lider`
        FOREIGN KEY (`lider`) REFERENCES `candidato`(`idCandidato`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1000;

CREATE TABLE IF NOT EXISTS `time_candidato` (
  `idTime` INT NOT NULL,
  `idCandidato` INT NOT NULL,
  PRIMARY KEY (`idTime`, `idCandidato`),
  CONSTRAINT `fk_time`
    FOREIGN KEY (`idTime`) REFERENCES `time`(`idTime`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_candidato`
    FOREIGN KEY (`idCandidato`) REFERENCES `candidato`(`idCandidato`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- --------------------------------------------------------

--
-- Estrutura da tabela `contest`
--

CREATE TABLE IF NOT EXISTS `contest` (
  `idContest` int(11) NOT NULL AUTO_INCREMENT,
  `nomeContest` varchar(200) NOT NULL,
  `status` enum('Ativo','Inativo') DEFAULT NULL,
  `loc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idContest`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

--
-- Extraindo dados da tabela `contest`
--

INSERT INTO `contest` (`idContest`, `nomeContest`, `status`, `loc`) VALUES
(1, 'Start Cup 2025', 'Ativo', 'Campus Party Goiânia 2025');

-- --------------------------------------------------------

--
-- Estrutura da tabela `desafios`
--

CREATE TABLE IF NOT EXISTS `desafios` (
  `idDesafio` int(11) NOT NULL AUTO_INCREMENT,
  `tituloDesafio` varchar(300) NOT NULL,
  `descricaoDesafio` varchar(300) NOT NULL,
  `idContest` int(11) NOT NULL,
  `status` enum('Ativo','Inativo') NOT NULL,
  `visibilidade` enum('Visivel', 'Invisivel') NOT NULL,
  `pontuacao` int(11) NOT NULL,
  PRIMARY KEY (`idDesafio`),
  KEY `fk_desafios_contest` (`idContest`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1000 ;

--
-- Extraindo dados da tabela `desafios`
--

INSERT INTO `desafios` (`idDesafio`, `tituloDesafio`, `descricaoDesafio`, `idContest`, `status`, `visibilidade`, `pontuacao`) VALUES
(1, 'Desafio teste', 'Desafio teste - Basta responder o nome do coordenador Victor Hugo', 1, 'Ativo', 'Visivel',1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `inativos`
--

CREATE TABLE IF NOT EXISTS `inativos` (
  `idInativos` int(11) NOT NULL AUTO_INCREMENT,
  `idDesafio` int(11) NOT NULL,
  PRIMARY KEY (`idInativos`),
  KEY `fk_inativos_desafios` (`idDesafio`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `respDesafio`
--

CREATE TABLE IF NOT EXISTS `respDesafio` (
  `idResp` int(11) NOT NULL AUTO_INCREMENT,
  `resposta` longtext NOT NULL,
  `idDesafio` int(11) DEFAULT NULL,
  PRIMARY KEY (`idResp`),
  KEY `fk_respDesafio_desafios` (`idDesafio`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `respostaSubmetida`
--

CREATE TABLE IF NOT EXISTS `respostaSubmetida` (
  `idRespSubmetida` int(11) NOT NULL AUTO_INCREMENT,
  `respostaSubmetida` longtext,
  `idCandidato` int(11) DEFAULT NULL,
  `idDesafio` int(11) DEFAULT NULL,
  PRIMARY KEY (`idRespSubmetida`),
  KEY `fk_respostaSubmetida_candidato` (`idCandidato`),
  KEY `fk_respostaSubmetida_desafios` (`idDesafio`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;



--
-- Limitadores para a tabela `acertoCandidato`
--
ALTER TABLE `acertoCandidato`
  ADD CONSTRAINT `fk_acertoCandidato_desafios` FOREIGN KEY (`idDesafio`) REFERENCES `desafios` (`idDesafio`),
  ADD CONSTRAINT `fk_acertoCandidato_respostaSubmetida` FOREIGN KEY (`idRespostaSubmetida`) REFERENCES `respostaSubmetida` (`idRespSubmetida`);

--
-- Limitadores para a tabela `desafios`
--
ALTER TABLE `desafios`
  ADD CONSTRAINT `fk_desafios_contest` FOREIGN KEY (`idContest`) REFERENCES `contest` (`idContest`);

--
-- Limitadores para a tabela `inativos`
--
ALTER TABLE `inativos`
  ADD CONSTRAINT `fk_inativos_desafios` FOREIGN KEY (`idDesafio`) REFERENCES `desafios` (`idDesafio`);

--
-- Limitadores para a tabela `respDesafio`
--
ALTER TABLE `respDesafio`
  ADD CONSTRAINT `fk_respDesafio_desafios` FOREIGN KEY (`idDesafio`) REFERENCES `desafios` (`idDesafio`);

--
-- Limitadores para a tabela `respostaSubmetida`
--
ALTER TABLE `respostaSubmetida`
  ADD CONSTRAINT `fk_respostaSubmetida_candidato` FOREIGN KEY (`idCandidato`) REFERENCES `candidato` (`idCandidato`),
  ADD CONSTRAINT `fk_respostaSubmetida_desafios` FOREIGN KEY (`idDesafio`) REFERENCES `desafios` (`idDesafio`);

SET CHARACTER_SET_CLIENT = NULL;



DELIMITER $$

CREATE TRIGGER trg_limite_membros_time
BEFORE INSERT ON time_candidato
FOR EACH ROW
BEGIN
  DECLARE qtd INT;
  SELECT COUNT(*) INTO qtd
  FROM time_candidato
  WHERE idTime = NEW.idTime;

  IF qtd >= 4 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Um time não pode ter mais que 4 candidatos.';
  END IF;
END$$

DELIMITER ;
