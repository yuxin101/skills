import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";

type ArticleAnalysis = {
  contentType: "technical" | "tutorial" | "methodology" | "narrative";
  purpose: "information" | "visualization" | "imagination";
  coreArguments: string[];
  illustrationPositions: IllustrationPosition[];
  recommendedDensity: "minimal" | "balanced" | "per-section" | "rich";
};

type IllustrationPosition = {
  index: number;
  section: string;
  paragraph: string;
  purpose: string;
  visualContent: string;
  filename: string;
};

export type OutlineData = {
  style: string;
  density: string;
  image_count: number;
  positions: IllustrationPosition[];
};

export function analyzeArticleContent(content: string): ArticleAnalysis {
  const sections = content.split(/^##+\s+/m).filter((s) => s.trim());
  const paragraphs = content.split(/\n\n+/).filter((p) => p.trim().length > 50);

  // Determine content type
  let contentType: ArticleAnalysis["contentType"] = "technical";
  const lowerContent = content.toLowerCase();
  if (lowerContent.includes("步骤") || lowerContent.includes("how to") || lowerContent.includes("tutorial")) {
    contentType = "tutorial";
  } else if (lowerContent.includes("方法") || lowerContent.includes("methodology") || lowerContent.includes("framework")) {
    contentType = "methodology";
  } else if (lowerContent.includes("故事") || lowerContent.includes("story") || lowerContent.includes("experience")) {
    contentType = "narrative";
  }

  // Determine purpose
  let purpose: ArticleAnalysis["purpose"] = "information";
  if (lowerContent.includes("设计") || lowerContent.includes("design") || lowerContent.includes("架构")) {
    purpose = "visualization";
  } else if (lowerContent.includes("想象") || lowerContent.includes("imagine") || lowerContent.includes("愿景")) {
    purpose = "imagination";
  }

  // Extract core arguments (simplified heuristic)
  const coreArguments: string[] = [];
  for (const section of sections.slice(0, 5)) {
    const heading = section.split("\n")[0]?.trim();
    if (heading && heading.length < 100) {
      coreArguments.push(heading.replace(/^#+\s*/, ""));
    }
  }

  // Identify illustration positions
  const positions: IllustrationPosition[] = [];
  let positionIndex = 0;

  // Simple pinyin mapping for common Chinese characters in tech articles
  const pinyinMap: Record<string, string> = {
    "观": "guan", "点": "dian", "核": "he", "心": "xin", "深": "shen", "度": "du",
    "分": "fen", "析": "xi", "从": "cong", "黑": "hei", "客": "ke", "松": "song",
    "冠": "guan", "军": "jun", "到": "dao", "星": "xing", "原": "yuan", "理": "li",
    "概": "gai", "念": "nian", "设": "she", "计": "ji", "争": "zheng", "议": "yi",
    "实": "shi", "践": "jian", "建": "jian", "价": "jia", "值": "zhi", "边": "bian",
    "界": "jie", "适": "shi", "用": "yong", "场": "chang", "景": "jing", "推": "tui",
    "荐": "jian", "模": "mo", "块": "kuai", "混": "hun", "合": "he", "策": "ce",
    "略": "lue", "架": "jia", "构": "gou", "优": "you", "化": "hua", "测": "ce",
    "试": "shi", "验": "yan", "证": "zheng", "安": "an", "全": "quan", "审": "shen",
    "查": "cha", "流": "liu", "水": "shui", "线": "xian", "持": "chi", "续": "xu",
    "学": "xue", "习": "xi", "生": "sheng", "命": "ming", "周": "zhou", "期": "qi",
    "事": "shi", "件": "jian", "处": "chu", "器": "qi", "斜": "xie", "杠": "gang",
    "指": "zhi", "令": "ling", "语": "yu", "言": "yan", "层": "ceng", "规": "gui",
    "范": "fan", "引": "yin", "擎": "qing", "编": "bian", "排": "pai", "部": "bu",
    "署": "shu", "环": "huan", "境": "jing", "变": "bian", "量": "liang", "切": "qie",
    "换": "huan", "自": "zi", "动": "dong", "兼": "jian", "容": "rong", "跨": "kua",
    "平": "ping", "台": "tai", "资": "zi", "产": "chan", "简": "jian", "单": "dan",
    "纯": "chun", "粹": "cui", "复": "fu", "杂": "za", "需": "xu", "求": "qiu",
    "关": "guan", "注": "zhu", "活": "huo", "跃": "yue", "讨": "tao", "论": "lun",
    "页": "ye", "新": "xin", "问": "wen", "题": "ti", "每": "mei", "天": "tian",
    "超": "chao", "过": "guo", "小": "xiao", "时": "shi", "尝": "chang", "试": "shi",
    "完": "wan", "整": "zheng", "装": "zhuang", "标": "biao", "准": "zhun", "差": "cha",
    "异": "yi", "势": "shi", "个": "ge", "人": "ren", "开": "kai", "发": "fa",
    "追": "zhui", "求": "qiu", "组": "zu", "反": "fan", "馈": "kui", "最": "zui",
    "好": "hao", "回": "hui", "顾": "gu", "总": "zong", "结": "jie", "一": "yi",
    "话": "hua", "代": "dai", "神": "shen", "器": "qi", "还": "hai", "是": "shi",
    "工": "gong", "程": "cheng", "明": "ming", "配": "pei", "置": "zhi", "可": "ke",
    "以": "yi", "系": "xi", "统": "tong", "但": "dan", "不": "bu", "等": "deng",
    "于": "yu", "所": "suo", "有": "you", "都": "dou", "要": "yao", "真": "zhen",
    "正": "zheng", "效": "xiao", "率": "lv", "来": "lai", "找": "zhao", "到": "dao",
    "你": "ni", "的": "de", "作": "zuo", "那": "na", "衡": "heng", "而": "er", "美": "mei",
    "诞": "dan", "故": "gu", "本": "ben", "身": "shen", "就": "jiu", "很": "hen",
    "能": "neng", "说": "shuo", "在": "zai", "中": "zhong", "内": "nei", "拿": "na",
    "下": "xia", "奖": "jiang", "金": "jin", "随": "sui", "后": "hou", "把": "ba",
    "月": "yue", "战": "zhan", "经": "jing", "验": "yan", "压": "ya", "缩": "suo",
    "成": "cheng", "套": "tao", "源": "yuan", "路": "lu", "径": "jing", "揭": "jie",
    "示": "shi", "了": "le", "趋": "qu", "熟": "shu", "练": "lian", "使": "shi",
    "用": "yong", "形": "xing", "己": "ji", "佳": "jia", "并": "bing", "图": "tu",
    "将": "jiang", "其": "qi", "包": "bao", "括": "kuo", "专": "zhuan", "职": "zhi",
    "子": "zi", "理": "li", "重": "chong", "定": "ding", "义": "yi", "按": "an",
    "码": "ma", "多": "duo", "扫": "sao", "描": "miao", "条": "tiao", "则": "ze",
    "项": "xiang", "覆": "fu", "盖": "gai", "亮": "liang", "与": "yu", "通": "tong",
    "无": "wu", "修": "xiu", "改": "gai", "文": "wen", "件": "jian", "调": "diao",
    "这": "zhe", "解": "jie", "决": "jue", "早": "zao", "版": "ban", "易": "yi",
    "冲": "chong", "突": "tu", "同": "tong", "跑": "pao", "四": "si", "大": "da",
    "上": "shang", "如": "ru", "今": "jin", "快": "kuai", "速": "su", "迭": "die",
    "体": "ti", "现": "xian", "前": "qian", "瞻": "zhan", "性": "xing", "即": "ji",
    "也": "ye", "高": "gao", "质": "zhi", "额": "e", "太": "tai", "容": "rong",
    "做": "zuo", "日": "ri", "常": "chang", "送": "song", "帮": "bang", "助": "zhu",
    "限": "xian", "周": "zhou", "只": "zhi", "几": "ji", "次": "ci", "参": "can",
    "考": "kao", "它": "ta", "写": "xie", "法": "fa", "即": "ji", "框": "kuang",
    "团": "tuan", "队": "dui", "始": "shi", "和": "he", "采": "cai", "果": "guo",
    "取": "qu", "混": "hun", "样": "yang", "负": "fu", "责": "ze", "确": "que",
    "保": "bao", "导": "dao", "出": "chu", "束": "shu", "更": "geng", "发": "fa",
    "进": "jin", "行": "xing", "信": "xin", "才": "cai", "报": "bao", "类": "lei",
    "并": "bing", "汉": "han", "数": "shu", "少": "shao", "错": "cuo", "误": "wu",
    "先": "xian", "硬": "ying", "凭": "ping", "注": "zhu", "入": "ru", "攻": "gong",
    "击": "ji", "败": "bai", "再": "zai", "搭": "da", "撰": "zhuan", "委": "wei",
    "派": "pai", "给": "gei", "阶": "jie", "段": "duan", "摘": "zhai", "要": "yao",
    "长": "chang", "丢": "diu", "失": "shi", "痛": "tong", "点": "dian", "斩": "zhan",
    "获": "huo", "因": "yin", "为": "wei", "它": "ta", "走": "zou", "向": "xiang",
    "当": "dang", "比": "bi", "很": "hen", "多": "duo", "项": "xiang", "目": "mu",
    "我": "wo", "们": "men", "制": "zhi", "造": "zao", "术": "shu", "债": "zhai",
    "网": "wang", "站": "zhan", "病": "bing", "毒": "du", "式": "shi", "传": "chuan",
    "播": "bo", "带": "dai", "面": "mian", "跃": "yue", "零": "ling", "星": "xing",
    "则": "ze", "群": "qun", "盲": "mang", "赢": "ying", "案": "an", "方": "fang",
    "票": "piao", "甚": "shen", "至": "zhi", "有": "you", "人": "ren", "在": "zai",
    "里": "li", "配": "pei", "置": "zhi", "把": "ba", "变": "bian", "更": "geng",
    "自": "zi", "动": "dong", "发": "fa", "送": "song", "到": "dao", "进": "jin",
    "行": "xing", "重": "chong", "查": "cha", "价": "jia", "值": "zhi", "某": "mou",
    "种": "zhong", "程": "cheng", "度": "du", "上": "shang", "是": "shi", "帮": "bang",
    "助": "zhu", "开": "kai", "发": "fa", "者": "zhe", "更": "geng", "高": "gao",
    "效": "xiao", "使": "shi", "用": "yong", "有": "you", "限": "xian", "写": "xie",
    "很": "hen", "便": "bian", "宜": "yi", "了": "le", "但": "dan", "好": "hao", "仍": "reng",
    "贵": "gui", "AI": "ai", "让": "rang", "几": "ji", "乎": "hu", "免": "mian",
    "费": "fei", "需": "xu", "要": "yao", "培": "pei", "养": "yang", "的": "de",
    "新": "xin", "习": "xi", "惯": "guan", "我": "wo", "实": "shi", "践": "jian",
    "建": "jian", "议": "yi", "最": "zui", "后": "hou", "先": "xian", "跑": "pao",
    "再": "zai", "说": "shuo", "原": "yuan", "则": "ze", "并": "bing", "行": "xing",
    "分": "fen", "支": "zhi", "强": "qiang", "制": "zhi", "清": "qing", "单": "dan",
    "文": "wen", "档": "dang", "即": "ji", "代": "dai", "码": "ma", "不": "bu",
    "是": "shi", "问": "wen", "题": "ti", "旧": "jiu", "习": "xi", "惯": "guan",
    "处": "chu", "理": "li", "新": "xin", "工": "gong", "具": "ju", "成": "cheng",
    "本": "ben", "思": "si", "维": "wei", "切": "qie", "换": "huan", "验": "yan",
    "证": "zheng", "MVP": "mvp", "原": "yuan", "型": "xing", "出": "chu", "来": "lai",
    "看": "kan", "效": "xiao", "果": "guo", "不": "bu", "同": "tong", "方": "fang",
    "案": "an", "各": "ge", "实": "shi", "现": "xian", "一": "yi", "遍": "bian",
    "对": "dui", "比": "bi", "后": "hou", "决": "jue", "定": "ding", "而": "er",
    "不": "bu", "是": "shi", "提": "ti", "前": "qian", "纠": "jiu", "结": "jie",
    "生": "sheng", "成": "cheng", "的": "de", "必": "bi", "须": "xu", "过": "guo",
    "这": "zhe", "几": "ji", "关": "guan", "能": "neng", "在": "zai", "秒": "miao",
    "内": "nei", "读": "du", "懂": "dong", "它": "ta", "在": "zai", "干": "gan",
    "嘛": "ma", "错": "cuo", "误": "wu", "处": "chu", "覆": "fu", "盖": "gai",
    "哪": "na", "些": "xie", "情": "qing", "况": "kuang", "有": "you", "对": "dui",
    "应": "ying", "的": "de", "测": "ce", "试": "shi", "吗": "ma", "如": "ru",
    "果": "guo", "半": "ban", "年": "nian", "后": "hou", "回": "hui", "来": "lai",
    "看": "kan", "我": "wo", "能": "neng", "快": "kuai", "速": "su", "理": "li",
    "解": "jie", "吗": "ma", "写": "xie", "的": "de", "文": "wen", "档": "dang",
    "要": "yao", "随": "sui", "代": "dai", "码": "ma", "一": "yi", "起": "qi",
    "审": "shen", "变": "bian", "了": "le", "没": "mei", "有": "you", "更": "geng",
    "新": "xin", "就": "jiu", "是": "shi", "技": "ji", "术": "shu", "债": "zhai",
    "转": "zhuan", "向": "xiang", "判": "pan", "断": "duan", "设": "she", "计": "ji",
    "维": "wei", "护": "hu", "还": "hai", "在": "zai", "真": "zhen", "正": "zheng",
    "效": "xiao", "率": "lv", "提": "ti", "升": "sheng", "承": "cheng", "认": "ren",
    "现": "xian", "实": "shi", "然": "ran", "后": "hou", "重": "chong", "新": "xin",
    "设": "she", "计": "ji", "我": "wo", "们": "men", "的": "de", "工": "gong",
    "作": "zuo", "流": "liu", "这": "zhe", "些": "xie", "最": "zui", "佳": "jia",
    "实": "shi", "践": "jian", "还": "hai", "在": "zai", "被": "bei", "整": "zheng",
    "个": "ge", "行": "xing", "业": "ye", "摸": "mo", "索": "suo", "中": "zhong",
    "每": "mei", "个": "ge", "人": "ren", "都": "dou", "是": "shi", "实": "shi",
    "验": "yan", "者": "zhe",
  };

  function toSlug(text: string): string {
    return text
      .split("")
      .map((char) => {
        const code = char.charCodeAt(0);
        if (code >= 0x4e00 && code <= 0x9fff) {
          // Chinese character
          return pinyinMap[char] || char;
        }
        return char.toLowerCase();
      })
      .join("")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 40) || "concept";
  }

  for (let i = 0; i < sections.length && positionIndex < 8; i++) {
    const section = sections[i]!;
    const sectionHeading = section.split("\n")[0]?.replace(/^#+\s*/, "").trim() || "";

    // Add illustration at key positions
    if (sectionHeading && positionIndex < sections.length) {
      positionIndex++;

      const filenameSlug = toSlug(sectionHeading);

      positions.push({
        index: positionIndex,
        section: sectionHeading,
        paragraph: `After "${sectionHeading}" section`,
        purpose: `Visualize key concept of ${sectionHeading}`,
        visualContent: `Illustrate the main idea of ${sectionHeading} in hand-drawn minimalist style`,
        filename: `${String(positionIndex).padStart(2, "0")}-hand-drawn-${filenameSlug}.png`,
      });
    }
  }

  // Recommend density
  let recommendedDensity: ArticleAnalysis["recommendedDensity"] = "balanced";
  if (sections.length <= 3) {
    recommendedDensity = "minimal";
  } else if (sections.length <= 6) {
    recommendedDensity = "balanced";
  } else if (sections.length <= 10) {
    recommendedDensity = "per-section";
  } else {
    recommendedDensity = "rich";
  }

  return {
    contentType,
    purpose,
    coreArguments,
    illustrationPositions: positions,
    recommendedDensity,
  };
}

function formatOutlineMarkdown(outline: OutlineData, articlePath: string): string {
  const frontmatter = `---
style: ${outline.style}
density: ${outline.density}
image_count: ${outline.image_count}
---

# Article Illustration Outline

Article: ${articlePath}
Style: Hand-drawn Minimalist
Density: ${outline.density}
Total Images: ${outline.image_count}

---

`;

  const positions = outline.positions
    .map(
      (pos) => `## Illustration ${pos.index}

**Position**: ${pos.section}
**Purpose**: ${pos.purpose}
**Visual Content**: ${pos.visualContent}
**Filename**: ${pos.filename}

---
`
    )
    .join("\n");

  return frontmatter + positions;
}

export async function generateOutline(
  articlePath: string,
  content: string,
  density: string,
  outputDir: string
): Promise<OutlineData> {
  const analysis = analyzeArticleContent(content);

  let positions = analysis.illustrationPositions;

  // Filter positions based on density
  if (density === "minimal") {
    positions = positions.slice(0, 2);
  } else if (density === "balanced") {
    positions = positions.slice(0, 4);
  } else if (density === "rich") {
    // Keep all positions
  }
  // per-section keeps all section-based positions

  const outline: OutlineData = {
    style: "hand-drawn",
    density,
    image_count: positions.length,
    positions,
  };

  // Save outline.md
  const outlineContent = formatOutlineMarkdown(outline, articlePath);
  await mkdir(outputDir, { recursive: true });
  await writeFile(path.join(outputDir, "outline.md"), outlineContent);

  return outline;
}

export async function generatePromptFiles(
  outline: OutlineData,
  articleContent: string,
  outputDir: string
): Promise<string[]> {
  const promptsDir = path.join(outputDir, "prompts");
  await mkdir(promptsDir, { recursive: true });

  const promptFiles: string[] = [];

  for (const position of outline.positions) {
    const promptContent = await buildHandDrawnPrompt(articleContent, position.visualContent, position.section);
    const filename = position.filename.replace(".png", ".md");
    const filePath = path.join(promptsDir, filename);

    const frontmatter = `---
illustration_id: ${position.index}
style: hand-drawn
---

`;

    const fullContent = frontmatter + promptContent;
    await writeFile(filePath, fullContent);
    promptFiles.push(filePath);
  }

  return promptFiles;
}

async function buildHandDrawnPrompt(articleContent: string, illustrationDesc: string, sectionTitle: string): Promise<string> {
  // Extract key terms from article for specific details
  const keyTerms = extractKeyTerms(articleContent);

  return `请生成一张手绘风格插图，用于文章章节「${sectionTitle}」的配图：

## 主题描述
${illustrationDesc}

## 核心元素
${keyTerms.elements.map((e) => `- ${e}`).join("\n") || "- 抽象概念可视化"}

## 色彩要求
- 主色调：${keyTerms.primaryColor}
- 辅助色：${keyTerms.accentColor}
- 色调统一，风格一致

## 风格要求
- 手绘风格，有手工绘制的质感
- 简约，不复杂
- 整洁，画面干净
- 适当留白，不要填满
- 构图平衡，视觉焦点清晰
- 色调统一，不要过于跳跃
- 不要包含任何文字

## 技术规格
- 横版构图 (16:9)
- 适合文章配图使用
- 便于排版的简洁设计`;
}

function extractKeyTerms(content: string): {
  primaryColor: string;
  accentColor: string;
  elements: string[];
} {
  const elements: string[] = [];
  const lowerContent = content.toLowerCase();

  // Extract potential labels (short quoted strings or key terms)
  const quoteMatches = content.match(/[""](.*?)[""]/g) || [];
  for (const quote of quoteMatches.slice(0, 5)) {
    const text = quote.replace(/[""']/g, "").trim();
    if (text.length > 1 && text.length < 30) {
      elements.push(text);
    }
  }

  // Determine colors based on content themes
  let primaryColor = "蓝色/青色系";
  let accentColor = "橙色/黄色系";

  if (lowerContent.includes("科技") || lowerContent.includes("tech") || lowerContent.includes("AI") || lowerContent.includes("代码")) {
    primaryColor = "蓝色/紫色系";
    accentColor = "青色/绿色系";
  } else if (lowerContent.includes("温暖") || lowerContent.includes("warm") || lowerContent.includes("story")) {
    primaryColor = "橙色/黄色系";
    accentColor = "红色/粉色调";
  } else if (lowerContent.includes("自然") || lowerContent.includes("nature") || lowerContent.includes("green")) {
    primaryColor = "绿色/青色系";
    accentColor = "黄色/橙色调";
  } else if (lowerContent.includes("商业") || lowerContent.includes("business") || lowerContent.includes("金融")) {
    primaryColor = "深蓝/灰色系";
    accentColor = "金色/橙色调";
  }

  return { primaryColor, accentColor, elements };
}
