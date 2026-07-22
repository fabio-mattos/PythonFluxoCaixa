WITH MOVIMENTOS AS
(
    -- CLT
    SELECT
        LR.IDProjetoRateio,
        YEAR(CAST(L.Data - 2 AS DATETIME)) AS Ano,
        MONTH(CAST(L.Data - 2 AS DATETIME)) AS Mes,
        SUM(LR.ValorRateio) AS TotalCLT,
        CAST(0 AS DECIMAL(18,2)) AS TotalPessoalNaoContratado
    FROM TBLancamento L (NOLOCK)
    INNER JOIN TBLancamentoRateio LR (NOLOCK)
        ON LR.IDLancamentoRateio = L.IDLancamento
    INNER JOIN TBProjeto P (NOLOCK)
        ON P.IDProjeto = LR.IDProjetoRateio
    WHERE L.IDCategoriaFinanceira IN (4,14)
      AND P.CodigoProjetoCompleto IN ('112024','622024','872024','502025','1142025','142026','152026')
      AND L.Data > 0
    GROUP BY
        LR.IDProjetoRateio,
        YEAR(CAST(L.Data - 2 AS DATETIME)),
        MONTH(CAST(L.Data - 2 AS DATETIME))

    UNION ALL

    -- Pessoal Não Contratado
    SELECT
        LR.IDProjetoRateio,
        YEAR(CAST(L.Data - 2 AS DATETIME)) AS Ano,
        MONTH(CAST(L.Data - 2 AS DATETIME)) AS Mes,
        CAST(0 AS DECIMAL(18,2)) AS TotalCLT,
        SUM(LR.ValorRateio) AS TotalPessoalNaoContratado
    FROM TBLancamento L (NOLOCK)
    INNER JOIN TBLancamentoRateio LR (NOLOCK)
        ON LR.IDLancamentoRateio = L.IDLancamento
    INNER JOIN TBProjeto P (NOLOCK)
        ON P.IDProjeto = LR.IDProjetoRateio
    WHERE L.IDCategoriaFinanceira IN (6,10,11)
      AND P.CodigoProjetoCompleto IN ('112024','622024','872024','502025','1142025','142026','152026')
      AND L.Data > 0
    GROUP BY
        LR.IDProjetoRateio,
        YEAR(CAST(L.Data - 2 AS DATETIME)),
        MONTH(CAST(L.Data - 2 AS DATETIME))
)

SELECT
    P.CodigoProjetoCompleto AS cdProjeto,
    M.Ano,
    M.Mes,
    FORMAT(SUM(M.TotalCLT),'N2','pt-BR') AS TotalCLT,
    FORMAT(SUM(M.TotalPessoalNaoContratado),'N2','pt-BR') AS TotalPessoalNaoContratado

FROM MOVIMENTOS M
INNER JOIN TBProjeto P (NOLOCK)
    ON P.IDProjeto = M.IDProjetoRateio

GROUP BY
    M.Ano,
    M.Mes,
    P.CodigoProjetoCompleto

ORDER BY
  P.CodigoProjetoCompleto,
  M.Ano,
  M.Mes
