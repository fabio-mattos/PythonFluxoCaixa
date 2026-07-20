WITH RECEITA AS
(
    SELECT
        LR.IDProjetoRateio,
        SUM(LR.ValorRateio) AS TotalReceita
    FROM TBLancamento L (NOLOCK)
    INNER JOIN TBLancamentoRateio LR (NOLOCK)
        ON LR.IDLancamentoRateio = L.IDLancamento
    INNER JOIN TBProjeto P (NOLOCK)
        ON P.IDProjeto = LR.IDProjetoRateio
    WHERE L.IDCategoriaFinanceira in(15,55)
      AND P.CodigoProjetoCompleto IN ('112024','622024','872024','502025','1142025','142026','152026')
      AND L.Data > 0
    GROUP BY LR.IDProjetoRateio
),
CLT AS
(
    SELECT
        LR.IDProjetoRateio,
        SUM(LR.ValorRateio) AS TotalCLT
    FROM TBLancamento L (NOLOCK)
    INNER JOIN TBLancamentoRateio LR (NOLOCK)
        ON LR.IDLancamentoRateio = L.IDLancamento
    INNER JOIN TBProjeto P (NOLOCK)
        ON P.IDProjeto = LR.IDProjetoRateio
    WHERE L.IDCategoriaFinanceira in(4,14)
      AND P.CodigoProjetoCompleto IN ('112024','622024','872024','502025','1142025','142026','152026')
      AND L.Data > 0
    GROUP BY LR.IDProjetoRateio
),
PESSOAL_NAO_CONTRATADO AS
(
    SELECT
        LR.IDProjetoRateio,
        SUM(LR.ValorRateio) AS TotalPessoalNaoContratado
    FROM TBLancamento L (NOLOCK)
    INNER JOIN TBLancamentoRateio LR (NOLOCK)
        ON LR.IDLancamentoRateio = L.IDLancamento
    INNER JOIN TBProjeto P (NOLOCK)
        ON P.IDProjeto = LR.IDProjetoRateio
    WHERE L.IDCategoriaFinanceira IN (6,10,11)
      AND P.CodigoProjetoCompleto IN ('112024','622024','872024','502025','1142025','142026','152026')
      AND L.Data > 0
    GROUP BY LR.IDProjetoRateio
),
REDOA AS
(
    SELECT
        LR.IDProjetoRateio,
        SUM(LR.ValorRateio) AS TotalRedoa
    FROM TBLancamento L (NOLOCK)
    INNER JOIN TBLancamentoRateio LR (NOLOCK)
        ON LR.IDLancamentoRateio = L.IDLancamento
    INNER JOIN TBProjeto P (NOLOCK)
        ON P.IDProjeto = LR.IDProjetoRateio
    WHERE L.IDCategoriaFinanceira = 26
      AND P.CodigoProjetoCompleto IN ('112024','622024','872024','502025','1142025','142026','152026')
      AND L.Data > 0
    GROUP BY LR.IDProjetoRateio
),
DESPESAS AS
(
    SELECT
        LR.IDProjetoRateio,
        SUM(LR.ValorRateio) AS TotalDespesas
    FROM TBLancamento L (NOLOCK)
    INNER JOIN TBLancamentoRateio LR (NOLOCK)        ON LR.IDLancamentoRateio = L.IDLancamento
    INNER JOIN TBProjeto P (NOLOCK)        ON P.IDProjeto = LR.IDProjetoRateio
    LEFT OUTER JOIN tbcategoriafinanceira tbcategoriafinanceira (NOLOCK) ON tbcategoriafinanceira.IDCategoriaFinanceira = L.IDCategoriaFinanceira 
    WHERE 
        tbcategoriafinanceira.receita = 0   
      AND  L.IDCategoriaFinanceira NOT IN(18,35,36)      
      AND P.CodigoProjetoCompleto IN ('112024','622024','872024','502025','1142025','142026','152026')
      AND L.Data > 0
      AND L.CreditoDebito = 2
    GROUP BY LR.IDProjetoRateio
)
SELECT
    P.CodigoProjetoCompleto AS cdProjeto,
    DB_DRHFLOW.DBO.FORMATA_PROJETO_GEMINI_RM(P.CodigoProjetoCompleto) AS PRJ,
    FORMAT(ISNULL(R.TotalReceita,0),'N2','pt-BR') AS TotalReceita,
    FORMAT(ISNULL(D.TotalDespesas,0),'N2','pt-BR') AS TotalDespesas,
    FORMAT(ISNULL( db_drhflow.dbo.TOTAL_CLT_PROJETO(DB_DRHFLOW.DBO.FORMATA_PROJETO_GEMINI_RM(P.CodigoProjetoCompleto)),0),'N2','pt-BR') AS TotalCLT,
    FORMAT(ISNULL(PNC.TotalPessoalNaoContratado,0),'N2','pt-BR') AS TotalPessoalNaoContratado,
    FORMAT(ISNULL(RD.TotalRedoa,0),'N2','pt-BR') AS TotalRedoa
FROM RECEITA R
LEFT JOIN CLT C
    ON C.IDProjetoRateio = R.IDProjetoRateio
LEFT JOIN DESPESAS D
    ON D.IDProjetoRateio = R.IDProjetoRateio
LEFT JOIN PESSOAL_NAO_CONTRATADO PNC
    ON PNC.IDProjetoRateio = R.IDProjetoRateio
LEFT JOIN REDOA RD
    ON RD.IDProjetoRateio = R.IDProjetoRateio
INNER JOIN TBProjeto P (NOLOCK)
    ON P.IDProjeto = R.IDProjetoRateio
ORDER BY P.CodigoProjetoCompleto;