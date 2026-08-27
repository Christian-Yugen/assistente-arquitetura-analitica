type UnknownRecord = Record<string, unknown>;

export type GuidanceCard = {
  label: string;
  definition: string;
  nextStep: string;
  count: number;
  confidence: number | null;
  formula?: string;
};

export type ModelingGuidance = {
  dimensions: GuidanceCard[];
  facts: GuidanceCard[];
  structuralReviews: GuidanceCard[];
  relationships: GuidanceCard[];
  metrics: GuidanceCard[];
  semanticSignals: GuidanceCard[];
};

const TABLE_TYPES: Record<string, Omit<GuidanceCard, "count" | "confidence"> & { section: "dimensions" | "facts" | "structuralReviews" }> = {
  dimension_standard_candidate: { section: "dimensions", label: "Dimensão candidata", definition: "Tabela de atributos para filtrar, agrupar e descrever os fatos.", nextStep: "Confirme se ela representa uma entidade de negócio estável antes de criar relações." },
  dimension_calendar_candidate: { section: "dimensions", label: "Dimensão calendário candidata", definition: "Estrutura temporal de apoio para análises por data, mês, trimestre e ano.", nextStep: "Confirme o calendário de negócio e a chave de data antes de conectá-la aos fatos." },
  fact_transactional_candidate: { section: "facts", label: "Fato transacional candidato", definition: "Tabela que tende a registrar eventos ou movimentos repetidos.", nextStep: "Defina o grão: o que exatamente uma linha representa antes de criar medidas." },
  fact_periodic_candidate: { section: "facts", label: "Fato periódico candidato", definition: "Tabela que tende a registrar valores por período de referência.", nextStep: "Confirme período, unidade de observação e o comportamento das medidas no tempo." },
  accumulated_snapshot_review_required: { section: "structuralReviews", label: "Possível snapshot acumulado", definition: "A estrutura pode representar valores acumulados ao longo do tempo, exigindo leitura especial de saldos.", nextStep: "Confirme se o valor é saldo, movimento ou acumulado antes de somar." },
  auxiliary_table_review_required: { section: "structuralReviews", label: "Tabela auxiliar a revisar", definition: "A estrutura pode servir de apoio técnico, e não necessariamente de fato ou dimensão final.", nextStep: "Defina se ela deve apenas apoiar transformações ou compor o modelo final." },
  bridge_table_review_required: { section: "structuralReviews", label: "Possível tabela ponte", definition: "A estrutura pode ser necessária para representar associações entre várias entidades.", nextStep: "Confirme a cardinalidade antes de criar uma relação muitos-para-muitos." },
  conformed_dimension_review_required: { section: "structuralReviews", label: "Dimensão compartilhada a revisar", definition: "A estrutura pode ser reutilizada por mais de um fato, mas ainda requer validação.", nextStep: "Confirme se a mesma entidade possui significado e chave consistentes em todos os usos." },
  degenerate_dimension_review_required: { section: "structuralReviews", label: "Dimensão degenerada a revisar", definition: "Um atributo pode permanecer no fato em vez de virar uma dimensão separada.", nextStep: "Confirme se o atributo identifica ou descreve o evento sem exigir tabela própria." },
  extractable_dimension_review_required: { section: "structuralReviews", label: "Dimensão extraível a revisar", definition: "Há indício de atributos repetidos que podem formar uma dimensão separada.", nextStep: "Valide a chave e os atributos antes de separar a tabela." },
  fact_without_defined_grain_candidate: { section: "structuralReviews", label: "Fato sem grão definido", definition: "A estrutura parece conter medidas, mas o significado de cada linha não foi confirmado.", nextStep: "Defina uma frase objetiva: “uma linha representa …” antes de modelar." },
  fact_without_measures_review_required: { section: "structuralReviews", label: "Fato sem medida clara", definition: "A tabela pode registrar eventos, mas ainda não há medida agregável confirmada.", nextStep: "Confirme contagens, valores ou indicadores que possam virar medidas." },
  flat_table_review_required: { section: "structuralReviews", label: "Tabela plana a revisar", definition: "A estrutura pode misturar atributos e eventos em uma mesma tabela.", nextStep: "Decida se a simplicidade é intencional ou se dimensões devem ser separadas." },
  missing_dimension_review_required: { section: "structuralReviews", label: "Dimensão possivelmente ausente", definition: "O fato pode depender de uma entidade que não aparece como estrutura própria.", nextStep: "Verifique se a entidade deve ser criada, fornecida em outra fonte ou mantida no fato." },
  mixed_table_review_required: { section: "structuralReviews", label: "Tabela mista a revisar", definition: "A estrutura pode reunir mais de um assunto ou granularidade.", nextStep: "Separe os assuntos somente após confirmar que não representam o mesmo evento." },
  parameter_table_review_required: { section: "structuralReviews", label: "Tabela de parâmetros a revisar", definition: "A estrutura pode representar regras ou parâmetros de negócio, não dados analíticos.", nextStep: "Defina se ela deve controlar filtros, metas ou regras de cálculo." },
  repeated_attributes_review_required: { section: "structuralReviews", label: "Atributos repetidos a revisar", definition: "Há indício de atributos que podem se repetir entre registros e merecem normalização.", nextStep: "Confirme se os atributos descrevem uma entidade independente antes de extrair uma dimensão." },
  role_dimension_review_required: { section: "structuralReviews", label: "Dimensão de papéis a revisar", definition: "Uma mesma dimensão pode cumprir papéis diferentes em um fato, especialmente em datas.", nextStep: "Confirme os papéis e mantenha relações inativas quando houver mais de uma data." },
  stored_measures_review_required: { section: "structuralReviews", label: "Medidas armazenadas a revisar", definition: "Há valores que podem ser medidas armazenadas, mas a agregação ainda precisa de confirmação.", nextStep: "Defina unidade, agregação permitida e filtros antes de criar DAX." },
  table_classification_undefined_candidate: { section: "structuralReviews", label: "Estrutura ainda indefinida", definition: "O motor não encontrou evidência suficiente para chamar esta estrutura de fato ou dimensão.", nextStep: "Inclua mais registros reais ou responda às perguntas de negócio antes de decidir." },
};

const RELATIONSHIP_TYPES: Record<string, Omit<GuidanceCard, "count" | "confidence">> = {
  one_to_many_relationship_candidate: { label: "Relação um-para-muitos candidata", definition: "Uma estrutura pode fornecer uma chave única para múltiplos registros de outra estrutura.", nextStep: "Confirme a unicidade da chave e crie relação de filtro simples no Power BI." },
  one_side_key_non_unique_candidate: { label: "Chave do lado “um” não única", definition: "A relação pretendida tem duplicidade no lado que deveria ser único.", nextStep: "Corrija ou deduplique a chave antes de conectar as tabelas." },
  orphan_reference_candidate: { label: "Referência sem correspondência", definition: "Há indício de referências que não encontram chave correspondente.", nextStep: "Corrija a integridade dos dados antes de ativar a relação." },
  many_to_many_relationship_candidate: { label: "Relação muitos-para-muitos candidata", definition: "As duas estruturas podem possuir valores repetidos para a mesma associação.", nextStep: "Valide se uma tabela ponte é necessária; não conecte diretamente sem essa decisão." },
  bridge_need_review_required: { label: "Necessidade de tabela ponte", definition: "A relação pode exigir uma ponte para evitar duplicação e filtros ambíguos.", nextStep: "Defina a chave da associação antes de modelar cardinalidade muitos-para-muitos." },
  direct_fact_to_fact_relationship_review_candidate: { label: "Ligação entre fatos a revisar", definition: "Há um possível vínculo direto entre duas tabelas de fatos.", nextStep: "Evite criar a relação diretamente até confirmar uma dimensão compartilhada ou ponte." },
  ambiguous_relationship_path_review_candidate: { label: "Caminho de filtro ambíguo", definition: "A relação pode criar mais de um caminho de filtro no modelo.", nextStep: "Mantenha um único caminho ativo e valide relações alternativas antes de ativá-las." },
  bidirectional_filter_review_candidate: { label: "Filtro bidirecional a revisar", definition: "O relacionamento pode exigir avaliação de direção de filtro.", nextStep: "Use filtro em uma direção por padrão; aplique bidirecional somente com justificativa validada." },
  composite_relationship_key_review_candidate: { label: "Chave composta a revisar", definition: "A associação pode depender da combinação de mais de uma chave.", nextStep: "Crie uma chave técnica apenas após confirmar as partes e a unicidade da combinação." },
  conformed_dimension_review_candidate: { label: "Dimensão compartilhada entre fatos", definition: "Uma dimensão pode ser comum a mais de um fato.", nextStep: "Confirme a semântica e a chave antes de reutilizá-la em múltiplas relações." },
};

const METRIC_TYPES: Record<string, Omit<GuidanceCard, "count" | "confidence">> = {
  sum_conceptual_metric_candidate: { label: "Soma candidata", definition: "Conceito de medida para acumular um valor confirmado.", nextStep: "Escolha a medida, unidade e filtros antes de usar a fórmula.", formula: "SUM(eligible_measure)" },
  count_conceptual_metric_candidate: { label: "Contagem candidata", definition: "Conceito de medida para contar registros no grão confirmado.", nextStep: "Defina o que deve ser contado e quais filtros se aplicam.", formula: "COUNT(eligible_entity)" },
  distinct_count_conceptual_metric_candidate: { label: "Contagem distinta candidata", definition: "Conceito de medida para contar entidades únicas.", nextStep: "Confirme a entidade e a regra de filtros antes de usar a fórmula.", formula: "DISTINCTCOUNT(eligible_entity)" },
  average_conceptual_metric_candidate: { label: "Média candidata", definition: "Conceito de medida para obter a média de um valor confirmado.", nextStep: "Defina unidade, população e filtros antes de usar a fórmula.", formula: "AVERAGE(eligible_measure)" },
  minmax_conceptual_metric_candidate: { label: "Mínimo e máximo candidatos", definition: "Conceito de medida para revisar extremos de um valor confirmado.", nextStep: "Defina medida, unidade e filtros antes de usar a fórmula.", formula: "MIN/MAX(eligible_measure)" },
  rate_conceptual_metric_candidate: { label: "Taxa candidata", definition: "Conceito de medida para dividir um numerador confirmado por um denominador confirmado.", nextStep: "Confirme numerador, denominador, unidade e regra de divisão por zero.", formula: "eligible_numerator / eligible_denominator" },
  completion_rate_conceptual_metric_candidate: { label: "Taxa de conclusão candidata", definition: "Conceito para medir a parcela de registros concluídos entre os elegíveis.", nextStep: "Confirme o que significa concluído e qual população é elegível.", formula: "completed_items / eligible_items" },
  absolute_delta_conceptual_metric_candidate: { label: "Variação absoluta candidata", definition: "Conceito para comparar valor atual e base de comparação.", nextStep: "Confirme os dois períodos ou cenários antes de usar a fórmula.", formula: "eligible_actual - eligible_baseline" },
  percentage_delta_conceptual_metric_candidate: { label: "Variação percentual candidata", definition: "Conceito para expressar a mudança proporcional entre atual e base.", nextStep: "Confirme período-base e trate base zero antes de usar a fórmula.", formula: "((eligible_actual - eligible_baseline) / eligible_baseline) * 100" },
  running_total_conceptual_metric_candidate: { label: "Acumulado no tempo candidato", definition: "Conceito para acumular uma medida conforme uma dimensão temporal confirmada.", nextStep: "Confirme calendário, ordem temporal e medida antes de usar a fórmula.", formula: "cumulative eligible_measure ordered by eligible_time" },
  weighted_average_conceptual_metric_candidate: { label: "Média ponderada candidata", definition: "Conceito que combina uma medida com peso confirmado.", nextStep: "Confirme medida, peso e escopo antes de usar a fórmula.", formula: "weighted_sum(eligible_measure, eligible_weight) / total(eligible_weight)" },
  semiadditive_conceptual_metric_candidate: { label: "Medida semiaditiva a revisar", definition: "O valor pode exigir soma por algumas dimensões e último valor no tempo.", nextStep: "Confirme o comportamento de saldo antes de escolher a agregação.", formula: "aggregate eligible_balance across confirmed non_time_dimensions at confirmed time_grain" },
  domain_metric_conceptual_metric_candidate: { label: "Métrica de negócio a definir", definition: "A fórmula depende de uma regra de negócio que o arquivo não confirma sozinho.", nextStep: "Defina regra, unidade e filtros com a área de negócio." },
  metric_insufficient_review_required: { label: "Métrica ainda não recomendada", definition: "Não há medida confirmada suficiente para propor cálculo.", nextStep: "Defina o que deve ser medido e o grão antes de criar DAX." },
  dax_template_review_required: { label: "Modelo DAX a revisar", definition: "Há um modelo genérico de fórmula, ainda sem nomes reais de tabela ou campo.", nextStep: "Substitua os marcadores somente após confirmar fato, dimensão e medida.", formula: "SUM([CONFIRMED_MEASURE])" },
};

const SEMANTIC_TYPES: Record<string, Omit<GuidanceCard, "count" | "confidence">> = {
  identifier_candidate: { label: "Possível identificador", definition: "Há um sinal estrutural de campo que pode identificar entidades ou registros.", nextStep: "Confirme unicidade e estabilidade antes de usá-lo como chave." },
  date_candidate: { label: "Possível data", definition: "Há sinal de campo temporal que pode apoiar calendário e análises de período.", nextStep: "Confirme formato, semântica e relação com a dimensão calendário." },
  quantity_candidate: { label: "Possível quantidade", definition: "Há sinal de valor numérico que pode representar quantidade.", nextStep: "Confirme unidade e agregação permitida." },
  currency_candidate: { label: "Possível valor monetário", definition: "Há sinal de valor que pode representar moeda.", nextStep: "Confirme moeda, escala e regra de soma." },
  percentage_candidate: { label: "Possível percentual", definition: "Há sinal de valor que pode representar percentual.", nextStep: "Confirme se é taxa, proporção ou percentual já agregado antes de somar." },
  actual_candidate: { label: "Possível valor realizado", definition: "Há sinal de valor observado ou realizado.", nextStep: "Defina comparação e período antes de criar variações." },
  target_or_forecast_candidate: { label: "Possível meta ou previsão", definition: "Há sinal de valor de meta ou projeção.", nextStep: "Confirme período, versão e regra de comparação com o realizado." },
};

function asRecord(value: unknown): UnknownRecord {
  return value && typeof value === "object" && !Array.isArray(value) ? value as UnknownRecord : {};
}

function asRecords(value: unknown): UnknownRecord[] {
  return Array.isArray(value) ? value.map(asRecord) : [];
}

function confidence(value: unknown): number | null {
  return typeof value === "number" && value >= 0 && value <= 1 ? value : null;
}

function addCard(target: Map<string, GuidanceCard>, type: unknown, rawConfidence: unknown, catalog: Record<string, Omit<GuidanceCard, "count" | "confidence">>) {
  if (typeof type !== "string") return;
  const definition = catalog[type];
  if (!definition) return;
  const existing = target.get(type);
  const nextConfidence = confidence(rawConfidence);
  target.set(type, existing ? { ...existing, count: existing.count + 1, confidence: existing.confidence ?? nextConfidence } : { ...definition, count: 1, confidence: nextConfidence });
}

function cardsFrom(map: Map<string, GuidanceCard>) {
  return Array.from(map.values()).sort((left, right) => left.label.localeCompare(right.label, "pt-BR"));
}

export function getModelingGuidance(payload: UnknownRecord): ModelingGuidance {
  const dimensions = new Map<string, GuidanceCard>();
  const facts = new Map<string, GuidanceCard>();
  const structuralReviews = new Map<string, GuidanceCard>();
  const relationships = new Map<string, GuidanceCard>();
  const metrics = new Map<string, GuidanceCard>();
  const semanticSignals = new Map<string, GuidanceCard>();

  for (const sheet of asRecords(payload.sheets)) {
    const classification = asRecord(sheet.classification);
    const type = classification.type;
    if (typeof type !== "string") continue;
    const specification = TABLE_TYPES[type];
    if (!specification) continue;
    const target = specification.section === "dimensions" ? dimensions : specification.section === "facts" ? facts : structuralReviews;
    addCard(target, type, classification.confidence, TABLE_TYPES);
  }
  for (const relationship of asRecords(payload.relationships)) addCard(relationships, relationship.relationship_type, relationship.confidence, RELATIONSHIP_TYPES);
  for (const metric of asRecords(payload.metrics)) addCard(metrics, metric.metric_type, metric.confidence, METRIC_TYPES);
  for (const signal of asRecords(payload.semantic_classifications)) addCard(semanticSignals, signal.semantic_type, signal.confidence, SEMANTIC_TYPES);

  return { dimensions: cardsFrom(dimensions), facts: cardsFrom(facts), structuralReviews: cardsFrom(structuralReviews), relationships: cardsFrom(relationships), metrics: cardsFrom(metrics), semanticSignals: cardsFrom(semanticSignals) };
}
