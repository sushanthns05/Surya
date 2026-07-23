const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  VerticalAlign, PageBreak, LevelFormat, Header, Footer, PageNumber,
  NumberFormat
} = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function heading(text, level = HeadingLevel.HEADING_1, center = false) {
  return new Paragraph({
    heading: level,
    alignment: center ? AlignmentType.CENTER : AlignmentType.LEFT,
    children: [new TextRun({ text, bold: true })]
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    alignment: opts.center ? AlignmentType.CENTER : opts.justify ? AlignmentType.JUSTIFIED : AlignmentType.LEFT,
    spacing: { line: 360, before: opts.spaceBefore ?? 80, after: opts.spaceAfter ?? 80 },
    children: [new TextRun({ text, bold: opts.bold, size: opts.size ?? 24, font: "Times New Roman" })]
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function sectionTitle(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 240, after: 240 },
    children: [new TextRun({ text, bold: true, size: 32, font: "Times New Roman", underline: {} })]
  });
}

function moduleTitle(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, size: 36, font: "Times New Roman" })]
  });
}

function moduleSubtitle(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 80, after: 200 },
    children: [new TextRun({ text, bold: true, size: 28, font: "Times New Roman" })]
  });
}

function bodyPara(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 80, after: 80 },
    indent: { left: opts.indent ?? 0 },
    children: [new TextRun({ text, size: 24, font: "Times New Roman", bold: opts.bold })]
  });
}

function numberedItem(num, text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 60, after: 60 },
    indent: { left: 720, hanging: 360 },
    children: [new TextRun({ text: `${num}. ${text}`, size: 24, font: "Times New Roman" })]
  });
}

function bulletItem(text) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 60, after: 60 },
    indent: { left: 720 },
    children: [new TextRun({ text: `\u2022  ${text}`, size: 24, font: "Times New Roman" })]
  });
}

function makeTable(rows, colWidths, headerRow = false) {
  return new Table({
    width: { size: colWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: colWidths,
    rows: rows.map((row, ri) =>
      new TableRow({
        children: row.map((cell, ci) =>
          new TableCell({
            borders,
            width: { size: colWidths[ci], type: WidthType.DXA },
            shading: (ri === 0 && headerRow) ? { fill: "D0D0D0", type: ShadingType.CLEAR } : undefined,
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: cell, bold: ri === 0 && headerRow, size: 22, font: "Times New Roman" })]
            })]
          })
        )
      })
    )
  });
}

// ─── COVER PAGE ───────────────────────────────────────────────────────────────
const coverPage = [
  new Paragraph({ spacing: { before: 200, after: 200 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text: "VISVESVARAYA TECHNOLOGICAL UNIVERSITY", bold: true, size: 28, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "\u201cJNANA SANGAMA\u201d, BELAGAVI - 590018.", bold: true, size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 240 },
    children: [new TextRun({ text: "2025-2026", bold: true, size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text: "A Report on", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "National Service Scheme (NSS)", bold: true, size: 32, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 240 },
    children: [new TextRun({ text: "\u2013 23NSSN03", bold: true, size: 28, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text: "Submitted in partial fulfilment for the award of the degree of", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "BACHELOR OF ENGINEERING", bold: true, size: 28, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "IN", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 240 },
    children: [new TextRun({ text: "INFORMATION SCIENCE & ENGINEERING", bold: true, size: 28, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text: "Submitted By", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "Sushanth N S", bold: true, size: 26, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 240 },
    children: [new TextRun({ text: "[1JB24IS157]", bold: true, size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text: "Under the Guidance of", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "Mr. Abhinand B V", bold: true, size: 26, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "Assistant Professor", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 240 },
    children: [new TextRun({ text: "Dept. of ISE, SJBIT", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text: "DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING", bold: true, size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "SJB INSTITUTE OF TECHNOLOGY", bold: true, size: 26, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "BGS Health and Education City, Kengeri, Bangalore-560060.", size: 24, font: "Times New Roman" })]
  }),
  pageBreak(),
];

// ─── CERTIFICATE PAGE ─────────────────────────────────────────────────────────
const certificatePage = [
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 40 },
    children: [new TextRun({ text: "|| Jai Sri Gurudev ||", size: 22, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text: "Sri Adichunchanagiri Shikshana Trust \u00ae", size: 22, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 40 },
    children: [new TextRun({ text: "S. J. B INSTITUTE OF TECHNOLOGY", bold: true, size: 30, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 60 },
    children: [new TextRun({ text: "BGS Health & Education City, Kengeri, Bengaluru-560060.", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 40, after: 120 },
    children: [new TextRun({ text: "DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING", bold: true, size: 24, font: "Times New Roman" })]
  }),
  sectionTitle("CERTIFICATE"),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 120, after: 240 },
    children: [new TextRun({
      text: "Certified that the NSS activity carried out by Sushanth N S bearing [1JB24IS157] is a bonafide student of SJB Institute of Technology in partial fulfillment for the award of \u201cBACHELOR OF ENGINEERING\u201d in INFORMATION SCIENCE AND ENGINEERING as prescribed by VISVESVARAYA TECHNOLOGICAL UNIVERSITY, BELAGAVI during the academic year 2025-2026. It is certified that all corrections/suggestions indicated for Internal Assessment have been incorporated in the Report deposited in the Departmental library. The NSS activity report has been approved as it satisfies the academic requirements concerning NSS activity prescribed for the said Degree.",
      size: 24, font: "Times New Roman"
    })]
  }),
  new Paragraph({ spacing: { before: 240, after: 240 }, children: [] }),
  makeTable(
    [
      ["Mr. Abhinand B V", "Dr. Gopala Krishna M T", "Dr. Mahendra Prashanth K V"],
      ["Assistant Professor", "Professor & Head", "Principal"],
      ["Dept. of ISE", "Dept. of ISE", "SJBIT, Bangalore"],
    ],
    [3000, 3000, 3000],
    false
  ),
  pageBreak(),
];

// ─── ACKNOWLEDGEMENT ──────────────────────────────────────────────────────────
const acknowledgementPage = [
  sectionTitle("ACKNOWLEDGEMENT"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  bodyPara("I would like to express my profound gratitude to His Divine Soul Jagadguru Padmabhushan Sri Sri Sri Dr. Balagangadharanatha Mahaswamiji and His Holiness Jagadguru Sri Sri Sri Dr. Nirmalanandanatha Swamiji for providing me with an opportunity to be a part of this esteemed institution."),
  bodyPara("I would also like to express my profound thanks to Revered Sri Sri Dr. Prakashnath Swamiji, Managing Director, SJB Institute of Technology, for his continuous support in providing amenities to carry out this NSS activity in this admired institution."),
  bodyPara("I want to express my sincere gratitude to Dr. Puttaraju, Academic Director, for their invaluable support and guidance throughout this project. Their encouragement, constructive feedback, and commitment to fostering academic excellence have been instrumental in shaping the direction and quality of this work."),
  bodyPara("I express my gratitude to Dr. K V Mahendra Prashanth, Principal, SJB Institute of Technology, for providing me excellent facilities and academic ambiance, which helped me in the satisfactory completion of NSS activity work."),
  bodyPara("I extend my sincere thanks to Dr. Babu N V, Academic Dean, SJB Institute of Technology for providing me with constant support throughout the period of my NSS activity work."),
  bodyPara("I extend my sincere thanks to Dr. Gopala Krishna M T, Professor & Head, Dept. of Information Science & Engineering for providing invaluable support throughout the period of my NSS activity."),
  bodyPara("I wish to express my heartfelt gratitude to my MC: Mandatory Course (Non-credit) Coordinator Mrs. Yamuna U, Assistant Professor, Dept. of ISE, for her valuable guidance, suggestions and cheerful encouragement during the NSS activity."),
  bodyPara("I wish to express my heartfelt gratitude to my Course Coordinator Mr. Abhinand B V, Assistant Professor, Dept. of ISE for his valuable guidance, suggestions and cheerful encouragement during the NSS activity."),
  new Paragraph({ spacing: { before: 240, after: 60 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "Regards,", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "Sushanth N S", bold: true, size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.RIGHT,
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text: "[1JB24IS157]", bold: true, size: 24, font: "Times New Roman" })]
  }),
  pageBreak(),
];

// ─── ABSTRACT ─────────────────────────────────────────────────────────────────
const abstractPage = [
  sectionTitle("ABSTRACT"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  bodyPara("This report documents the National Service Scheme (NSS) activities undertaken by Sushanth N S (USN: 1JB24IS157), a student of the Department of Information Science and Engineering, SJB Institute of Technology, Bengaluru, during the academic year 2025-2026 as part of the course 23NSSN03."),
  bodyPara("The NSS is a voluntary public service program of the Government of India, aimed at developing the personality and character of students through community service. This report covers five key modules: NSS and Disaster Management, Social Building and National Integration, Awareness Programmes, Off-Campus Activities, and Campus Activities."),
  bodyPara("Through participation in various NSS activities including awareness drives, plantation drives (Shramadhan), seminars, workshops, rally programs, and visits to adopted villages, the student has developed a deeper sense of social responsibility, civic engagement, and community service. The report presents the activities undertaken, their impact, and the learnings derived from each module."),
  pageBreak(),
];

// ─── TABLE OF CONTENTS ────────────────────────────────────────────────────────
const tocPage = [
  sectionTitle("TABLE OF CONTENTS"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Chapter No.", "Particulars", "Page No."],
      ["", "Acknowledgement", "i"],
      ["", "Abstract", "ii"],
      ["", "Table of Contents", "iii"],
      ["", "List of Figures", "iv"],
      ["", "List of Tables", "v"],
      ["", "List of Abbreviations", "vi"],
      ["1", "Module 1: NSS and Disaster Management", "1"],
      ["2", "Module 2: Social Building and National Integration", "8"],
      ["3", "Module 3: Awareness Programmes", "14"],
      ["4", "Module 4: Off Campus Activities", "20"],
      ["5", "Module 5: Campus Activities", "26"],
      ["", "References", "32"],
    ],
    [1500, 5860, 2000],
    true
  ),
  pageBreak(),
];

// ─── LIST OF FIGURES ──────────────────────────────────────────────────────────
const listOfFigures = [
  sectionTitle("LIST OF FIGURES"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Figure No.", "Figure Name", "Page No."],
      ["1.1", "Types of Natural Disasters", "3"],
      ["1.2", "NSS Disaster Management Training", "5"],
      ["2.1", "National Integration Rally", "10"],
      ["2.2", "Community Social Building Activity", "12"],
      ["3.1", "Environment Awareness Drive", "16"],
      ["3.2", "Health & Hygiene Awareness Programme", "18"],
      ["4.1", "Rally Programme", "22"],
      ["4.2", "Village Visit - Jatha", "24"],
      ["5.1", "Shramadhan - Plantation Drive", "28"],
      ["5.2", "NSS Seminar Workshop", "30"],
    ],
    [1500, 5860, 2000],
    true
  ),
  pageBreak(),
];

// ─── LIST OF TABLES ───────────────────────────────────────────────────────────
const listOfTables = [
  sectionTitle("LIST OF TABLES"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Table No.", "Table Name", "Page No."],
      ["1.1", "Types of Disasters and Their Characteristics", "4"],
      ["2.1", "NSS Activities for National Integration", "11"],
      ["3.1", "Awareness Programme Summary", "15"],
      ["4.1", "Off-Campus Activity Log", "21"],
      ["5.1", "Campus Activity Schedule", "27"],
    ],
    [1500, 5860, 2000],
    true
  ),
  pageBreak(),
];

// ─── LIST OF ABBREVIATIONS ────────────────────────────────────────────────────
const listOfAbbreviations = [
  sectionTitle("LIST OF ABBREVIATIONS"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Sl. No.", "Abbreviation", "Stands For"],
      ["1", "NSS", "National Service Scheme"],
      ["2", "VTU", "Visvesvaraya Technological University"],
      ["3", "SJBIT", "SJB Institute of Technology"],
      ["4", "ISE", "Information Science and Engineering"],
      ["5", "NCMC", "Non-Credit Mandatory Course"],
      ["6", "NGO", "Non-Governmental Organization"],
      ["7", "CIE", "Continuous Internal Evaluation"],
      ["8", "USN", "University Seat Number"],
    ],
    [1200, 2500, 5660],
    true
  ),
  pageBreak(),
];

// ─── MODULE 1 ─────────────────────────────────────────────────────────────────
const module1 = [
  moduleTitle("Module - 1"),
  moduleSubtitle("NSS and Disaster Management"),
  heading("1.1 Introduction to Disaster: Meaning and Nature", HeadingLevel.HEADING_2),
  bodyPara("A disaster is a serious disruption of the functioning of a community or a society involving widespread human, material, economic or environmental losses and impacts, which exceeds the ability of the affected community or society to cope using its own resources. The word \u201cdisaster\u201d originates from the Latin term \u201cdesastre\u201d, meaning \u201cbad star\u201d, reflecting the ancient belief that negative celestial events caused catastrophes."),
  bodyPara("Disasters are characterized by their sudden or gradual onset, extensive impact on life and property, and their capacity to overwhelm normal societal functioning. They may arise from natural forces or as a result of human activities, and often require external assistance for recovery."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("1.2 Types of Disasters", HeadingLevel.HEADING_2),
  bodyPara("Disasters are broadly classified into natural disasters and man-made disasters. The following are major types:"),
  new Paragraph({ spacing: { before: 60, after: 60 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 60, after: 40 },
    children: [new TextRun({ text: "1. Floods:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("Floods occur when water overflows onto normally dry land. They are one of the most common and widespread natural hazards in India. Floods are caused by heavy rainfall, overflowing rivers, breaching of dams, or storm surges. They cause massive displacement of population, loss of life, damage to infrastructure, and spread of waterborne diseases."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 60, after: 40 },
    children: [new TextRun({ text: "2. Earthquakes:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("Earthquakes are violent tremors of the earth\u2019s surface caused by the movement of tectonic plates beneath the earth\u2019s crust. They can cause devastating damage to buildings, infrastructure, and human lives. India lies in one of the world\u2019s most seismically active regions, making earthquake preparedness a national priority."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 60, after: 40 },
    children: [new TextRun({ text: "3. Fires:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("Fire disasters can occur in forests, residential areas, industrial establishments, and public buildings. Uncontrolled fires lead to massive destruction of property, biodiversity loss, and loss of human life. Causes include electrical short circuits, industrial accidents, negligence, and forest fires during summer."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 60, after: 40 },
    children: [new TextRun({ text: "4. Accidents:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("Accidents encompass road accidents, rail disasters, industrial accidents, mine collapses, and building collapses. India records one of the highest rates of road accidents in the world. These events often demand quick emergency response and rescue operations."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 60, after: 40 },
    children: [new TextRun({ text: "5. Diseases (Epidemics and Pandemics):", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("Disease outbreaks such as cholera, dengue, malaria, and COVID-19 are classified as biological disasters. They spread rapidly through communities, overwhelming healthcare systems and resulting in large-scale morbidity and mortality. Prevention through hygiene, vaccination, and awareness is key to managing disease disasters."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("1.3 Role of NSS in Disaster Management", HeadingLevel.HEADING_2),
  bodyPara("The National Service Scheme plays a vital role in disaster preparedness, response, and rehabilitation. NSS volunteers are trained to act swiftly and responsibly during emergencies. Key roles include:"),
  bulletItem("Raising awareness among communities about disaster preparedness and safety protocols."),
  bulletItem("Participating in mock drills and first-aid training programs organized by civil authorities."),
  bulletItem("Assisting in relief operations during floods, earthquakes, and other disasters by distributing food, water, and essential supplies."),
  bulletItem("Supporting search and rescue operations under the supervision of trained disaster management personnel."),
  bulletItem("Helping in the rehabilitation of displaced communities by organizing temporary shelters and community support services."),
  bulletItem("Spreading awareness about disease prevention and proper sanitation in post-disaster environments."),
  bodyPara("NSS volunteers serve as a bridge between government disaster management agencies and affected communities, ensuring that relief reaches the most vulnerable sections of society. Their training in disaster management not only builds personal resilience but also contributes significantly to national disaster preparedness."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Disaster Type", "Primary Cause", "Impact Area", "NSS Role"],
      ["Flood", "Heavy Rainfall", "Riverine Regions", "Rescue & Relief"],
      ["Earthquake", "Tectonic Movement", "Seismic Zones", "Search & Rescue"],
      ["Fire", "Electrical/Human Error", "Urban/Forest Areas", "Evacuation Aid"],
      ["Accident", "Human Error/Negligence", "Roads/Industries", "First Aid"],
      ["Disease", "Biological Agents", "Dense Populations", "Awareness & Hygiene"],
    ],
    [2000, 2000, 2000, 3360],
    true
  ),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text: "Table 1.1: Types of Disasters and Their Characteristics", italics: true, size: 22, font: "Times New Roman" })]
  }),
  pageBreak(),
];

// ─── MODULE 2 ─────────────────────────────────────────────────────────────────
const module2 = [
  moduleTitle("Module - 2"),
  moduleSubtitle("Social Building and National Integration"),
  heading("2.1 Social Building: Meaning and Nature", HeadingLevel.HEADING_2),
  bodyPara("Social building refers to the process of strengthening the social fabric of a community or nation by fostering cooperation, mutual trust, shared values, and a sense of collective identity. It involves developing institutions, relationships, and norms that bind people together and enable them to work collectively toward common goals."),
  bodyPara("The nature of social building is inclusive and participatory. It seeks to eliminate disparities based on caste, religion, gender, and economic status, and promotes equal opportunities for all citizens. Social building includes activities such as community development programs, social welfare schemes, inclusive education, healthcare access, and building inter-community relations."),
  bodyPara("For a diverse country like India, social building is particularly crucial. With hundreds of languages, religions, and cultural traditions, building a cohesive society requires deliberate and sustained effort at all levels \u2013 from schools and colleges to government institutions."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("2.2 National Integration: Meaning and Nature", HeadingLevel.HEADING_2),
  bodyPara("National integration is the process of bringing together diverse groups of people with different linguistic, religious, cultural, and regional identities into a unified national community bound by shared values, common goals, and a sense of belonging to one nation."),
  bodyPara("In the Indian context, national integration means transcending differences of caste, creed, religion, and language to forge a unified identity as Indians. It involves both political integration (unifying the political structures of the nation) and social integration (building harmony among diverse communities)."),
  bodyPara("The nature of national integration is dynamic and ongoing. It cannot be achieved once and for all but requires continuous reinforcement through education, cultural exchange, intermingling of communities, and strong democratic institutions. National integration is strengthened by equal rights and justice for all citizens under the Constitution of India."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("2.3 Role of Youth in Nation Building", HeadingLevel.HEADING_2),
  bodyPara("Youth are the most powerful agents of social change and nation building. With energy, creativity, and an open mind, young people are uniquely positioned to lead transformative change in society. The role of youth in nation building includes:"),
  numberedItem(1, "Education and Literacy: Educated youth contribute to human capital development, driving economic growth and social progress."),
  numberedItem(2, "Social Awareness: Youth can raise awareness about critical issues such as environmental conservation, gender equality, and public health through campaigns, social media, and community engagement."),
  numberedItem(3, "Political Participation: Active participation in democratic processes \u2013 voting, civic activism, and political discourse \u2013 strengthens governance and accountability."),
  numberedItem(4, "Entrepreneurship and Innovation: Young entrepreneurs create jobs, drive technological innovation, and contribute to economic development."),
  numberedItem(5, "Community Service: Through programs like NSS and NCC, youth directly serve communities, contributing to nation building at the grassroots level."),
  numberedItem(6, "Cultural Exchange: Youth facilitate cultural exchange across regions and communities, fostering a spirit of national integration and mutual respect."),
  bodyPara("The NSS program embodies the vision of youth-led nation building by engaging students in meaningful community service, social awareness activities, and leadership development programs."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Sl. No.", "NSS Activity", "Objective", "Beneficiaries"],
      ["1", "National Integration Rally", "Promote unity in diversity", "Students & Community"],
      ["2", "Cultural Programme", "Foster cultural exchange", "College Campus"],
      ["3", "Social Awareness Drive", "Build social consciousness", "Local Community"],
      ["4", "Community Service", "Strengthen social fabric", "Villages & Slums"],
      ["5", "Constitution Day Celebration", "Civic education", "Students"],
    ],
    [900, 2500, 2500, 3460],
    true
  ),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text: "Table 2.1: NSS Activities for National Integration", italics: true, size: 22, font: "Times New Roman" })]
  }),
  pageBreak(),
];

// ─── MODULE 3 ─────────────────────────────────────────────────────────────────
const module3 = [
  moduleTitle("Module - 3"),
  moduleSubtitle("Awareness Programmes"),
  heading("3.1 Awareness Programmes at Village/Slum Level", HeadingLevel.HEADING_2),
  bodyPara("Awareness programmes constitute one of the most impactful activities of the NSS. These programmes are conducted in villages, slums, and peri-urban areas to educate and sensitize communities on critical issues affecting their health, environment, and well-being."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 80, after: 40 },
    children: [new TextRun({ text: "A. Environment Conservation:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("NSS volunteers conduct awareness drives on the importance of protecting the natural environment. Activities include tree plantation drives, anti-littering campaigns, awareness walks about deforestation and its consequences, and sensitization on water conservation. Volunteers explain the need to reduce plastic use and promote organic waste management."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 80, after: 40 },
    children: [new TextRun({ text: "B. Sustainable Energy Sources:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("Programmes are conducted to educate villagers and slum dwellers about sustainable energy alternatives. NSS volunteers explain the benefits of solar energy, biogas plants, and energy-efficient cooking stoves. These awareness drives aim to reduce dependence on fossil fuels and non-renewable energy sources."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 80, after: 40 },
    children: [new TextRun({ text: "C. Waste Management:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("NSS volunteers educate communities on the principles of waste segregation \u2013 separating wet/organic waste from dry/recyclable waste. Awareness about composting, recycling, and responsible disposal of hazardous waste is provided. Villages are encouraged to set up community composting units as a sustainable waste management solution."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 80, after: 40 },
    children: [new TextRun({ text: "D. Health Awareness:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("Health camps are organized in villages and slums to provide basic health check-ups, awareness about common diseases, and information on government health schemes. NSS volunteers distribute literature on personal hygiene, hand washing, dental care, and mental health awareness."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("3.2 Family Welfare and Nutrition Programmes for Women and Children", HeadingLevel.HEADING_2),
  bodyPara("NSS volunteers conduct specialized awareness programmes targeting women and children in rural and semi-urban communities. These programmes address critical issues related to family welfare and nutrition:"),
  bulletItem("Maternal Health: Educating pregnant women and new mothers about prenatal care, safe delivery practices, breastfeeding, and postnatal care."),
  bulletItem("Child Nutrition: Spreading awareness about balanced diet, importance of micronutrients (iron, calcium, vitamins), and combating malnutrition among children under five."),
  bulletItem("Girl Child Education: Encouraging families to send girl children to school and emphasizing the importance of female education for community development."),
  bulletItem("Immunization Drives: Assisting government health workers in organizing immunization camps for children."),
  bulletItem("Sanitation and Hygiene: Educating families about the importance of clean sanitation facilities, proper hand-washing, and menstrual hygiene for women and girls."),
  bulletItem("Government Scheme Awareness: Informing communities about schemes such as Pradhan Mantri Matru Vandana Yojana, Poshan Abhiyan, and Swachh Bharat Mission."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Programme", "Target Group", "Key Message", "Outcome"],
      ["Environment Awareness Drive", "Village/Slum Community", "Protect nature, reduce waste", "Cleaner surroundings"],
      ["Health Camp", "All Community Members", "Hygiene & Disease Prevention", "Improved health awareness"],
      ["Nutrition Programme", "Women & Children", "Balanced diet & immunization", "Reduced malnutrition"],
      ["Sanitation Drive", "Households", "Clean sanitation & hygiene", "Behaviour change"],
    ],
    [2100, 2000, 2200, 3060],
    true
  ),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text: "Table 3.1: Awareness Programme Summary", italics: true, size: 22, font: "Times New Roman" })]
  }),
  pageBreak(),
];

// ─── MODULE 4 ─────────────────────────────────────────────────────────────────
const module4 = [
  moduleTitle("Module - 4"),
  moduleSubtitle("Off Campus Activities"),
  heading("4.1 Rally Programmes", HeadingLevel.HEADING_2),
  bodyPara("Rally programmes are one of the most visible and impactful off-campus activities of NSS. Rallies are organized on important national and international days to create public awareness on issues of social, environmental, and national significance. NSS volunteers march through streets, public places, and residential areas carrying banners, placards, and shouting awareness slogans."),
  bodyPara("Rally programmes conducted during the academic year 2025-2026 included:"),
  bulletItem("Republic Day Rally (26th January 2026): A patriotic rally organized in collaboration with local civic bodies to celebrate national unity and honor the Constitution of India."),
  bulletItem("World Environment Day Rally (5th June 2025): An awareness rally to sensitize the public on environmental conservation and climate change, with participation from local schools and community organizations."),
  bulletItem("Anti-Drug Awareness Rally: A rally to spread awareness about the harmful effects of substance abuse and drug addiction, encouraging youth to lead a healthy lifestyle."),
  bulletItem("Swachh Bharat Rally: A cleanliness drive rally promoting the objectives of the Swachh Bharat Mission and encouraging communities to maintain clean surroundings."),
  bodyPara("Rallies effectively mobilize public attention and create a powerful impact through collective participation. They demonstrate the NSS\u2019s commitment to community welfare and social consciousness."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("4.2 Jatha \u2013 Visit to Adopted Villages", HeadingLevel.HEADING_2),
  bodyPara("The Jatha is a traditional NSS activity involving a procession of volunteers to adopted villages for community service and awareness activities. Under the NSS program at SJBIT, the unit has adopted a village near Bengaluru for regular visits and community engagement."),
  bodyPara("During Jatha visits, NSS volunteers undertake a range of activities including:"),
  bulletItem("Cleanliness drives in the village, cleaning public spaces, roads, and water bodies."),
  bulletItem("Door-to-door health and hygiene awareness campaigns."),
  bulletItem("Distribution of informational pamphlets on government welfare schemes."),
  bulletItem("Interaction with village panchayat members to understand community needs."),
  bulletItem("Awareness programmes for women on maternal health, nutrition, and sanitation."),
  bulletItem("Tree plantation in the village to promote environmental conservation."),
  bodyPara("These visits provide NSS volunteers with direct exposure to rural life and its challenges, fostering empathy, social awareness, and a deeper understanding of community development issues."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("4.3 Visit and Conservation of Ancient Monuments and Heritage Sites", HeadingLevel.HEADING_2),
  bodyPara("India is home to thousands of ancient monuments and heritage sites that bear testimony to its rich cultural and historical legacy. NSS volunteers participate in heritage conservation activities to protect and preserve these national treasures for future generations."),
  bodyPara("Activities undertaken during the academic year include:"),
  bulletItem("Visit to historical monuments in and around Bengaluru to understand their historical and cultural significance."),
  bulletItem("Cleanliness drives at heritage sites to remove litter and maintain their pristine condition."),
  bulletItem("Creating awareness among local communities and tourists about responsible behaviour at heritage sites."),
  bulletItem("Documentation of local heritage through photography and written reports."),
  bodyPara("Heritage conservation activities sensitize NSS volunteers to the importance of cultural preservation and develop pride in India\u2019s rich civilizational heritage."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Activity", "Date", "Venue", "Participants", "Outcome"],
      ["Republic Day Rally", "26-Jan-2026", "Kengeri, Bengaluru", "75", "Patriotic awareness"],
      ["Environment Day Rally", "05-Jun-2025", "College Campus & Locality", "80", "Environmental sensitization"],
      ["Jatha Village Visit", "Nov 2025", "Adopted Village", "60", "Community service"],
      ["Heritage Site Visit", "Dec 2025", "Historical Monument", "50", "Heritage awareness"],
      ["Anti-Drug Rally", "Jan 2026", "Kengeri Area", "90", "Drug awareness"],
    ],
    [2000, 1500, 2200, 1200, 2460],
    true
  ),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text: "Table 4.1: Off-Campus Activity Log", italics: true, size: 22, font: "Times New Roman" })]
  }),
  pageBreak(),
];

// ─── MODULE 5 ─────────────────────────────────────────────────────────────────
const module5 = [
  moduleTitle("Module - 5"),
  moduleSubtitle("Campus Activities"),
  heading("5.1 Shramadhan \u2013 Plantation and Watering", HeadingLevel.HEADING_2),
  bodyPara("Shramadhan, meaning \u201cthe donation of labor,\u201d is a cornerstone of NSS campus activities. It involves voluntary physical labor for community benefit without any monetary reward, embodying the spirit of selfless service that lies at the heart of the NSS ethos."),
  bodyPara("At SJBIT, Shramadhan activities are primarily focused on plantation drives and maintaining the college\u2019s green cover. Activities include:"),
  bulletItem("Tree Plantation Drive: NSS volunteers plant saplings across the college campus, residential areas, and nearby public spaces. Saplings of native tree species are preferred to support local biodiversity."),
  bulletItem("Watering and Maintenance: Volunteers take responsibility for regularly watering newly planted saplings and maintaining their growth until they are well established."),
  bulletItem("Campus Cleaning: Shramadhan activities also include cleaning the college campus, removing waste, and maintaining the environment."),
  bulletItem("Garden Development: Developing and maintaining herbal and flower gardens on campus to beautify the environment and raise awareness about medicinal plants."),
  bodyPara("Shramadhan activities instill in students a deep respect for nature, a sense of environmental responsibility, and the value of physical labor in community service. The college campus has significantly improved its green cover owing to sustained Shramadhan efforts."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  heading("5.2 Awareness Programmes \u2013 Seminars, Workshops, and National/International Days", HeadingLevel.HEADING_2),
  bodyPara("Campus-based awareness programmes are organized regularly as part of NSS activities. These include seminars, workshops, and events commemorating national and international days of significance."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 80, after: 40 },
    children: [new TextRun({ text: "A. Seminars and Workshops:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bodyPara("NSS volunteers organize and participate in seminars and workshops on topics including disaster management, environmental conservation, health and hygiene, gender equality, digital literacy, and career guidance. These events feature expert speakers, interactive sessions, and group discussions that broaden students\u2019 knowledge and social awareness."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 80, after: 40 },
    children: [new TextRun({ text: "B. Celebration of National Days:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bulletItem("Independence Day (15th August): Flag hoisting ceremony followed by cultural programmes and patriotic speeches."),
  bulletItem("Republic Day (26th January): Constitution reading and awareness about fundamental rights and duties."),
  bulletItem("Gandhi Jayanti (2nd October): Cleanliness drive and Swachh Bharat awareness activities."),
  bulletItem("National Voters\u2019 Day (25th January): Awareness about voting rights and the importance of democratic participation."),
  new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 360, before: 80, after: 40 },
    children: [new TextRun({ text: "C. Celebration of International Days:", bold: true, size: 24, font: "Times New Roman" })]
  }),
  bulletItem("World Environment Day (5th June): Tree plantation and environmental awareness campaigns."),
  bulletItem("World Health Day (7th April): Health camps and awareness on preventive healthcare."),
  bulletItem("World AIDS Day (1st December): Awareness drives on HIV/AIDS prevention and reducing stigma."),
  bulletItem("International Day of Yoga (21st June): Yoga sessions and awareness on holistic well-being."),
  bodyPara("These campus activities ensure that NSS volunteers remain engaged, informed, and active participants in building a socially responsible and environmentally conscious college community."),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  makeTable(
    [
      ["Activity", "Date", "Type", "Participants", "Theme"],
      ["Shramadhan - Plantation", "Jul 2025", "Campus Activity", "100", "Green Campus"],
      ["Independence Day", "15-Aug-2025", "National Day", "200+", "Patriotism"],
      ["Gandhi Jayanti Drive", "02-Oct-2025", "National Day", "80", "Swachh Bharat"],
      ["World Health Day Camp", "07-Apr-2026", "International Day", "60", "Preventive Health"],
      ["NSS Day Seminar", "24-Sep-2025", "Seminar", "75", "Community Service"],
      ["Yoga Day", "21-Jun-2025", "International Day", "150", "Holistic Wellness"],
    ],
    [2200, 1500, 1800, 1200, 2660],
    true
  ),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text: "Table 5.1: Campus Activity Schedule", italics: true, size: 22, font: "Times New Roman" })]
  }),
  pageBreak(),
];

// ─── CONCLUSION ───────────────────────────────────────────────────────────────
const conclusionPage = [
  sectionTitle("CONCLUSION"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  bodyPara("The National Service Scheme (NSS) program at SJB Institute of Technology has provided an invaluable platform for developing social consciousness, leadership skills, and a spirit of community service. Through active participation in the five modules covering Disaster Management, Social Building and National Integration, Awareness Programmes, Off-Campus Activities, and Campus Activities, the experience has been both enriching and transformative."),
  bodyPara("The disaster management module equipped volunteers with the knowledge and skills to respond effectively to emergencies, understand the nature of various disasters, and contribute to community resilience. The Social Building and National Integration module reinforced the importance of unity in diversity and the critical role that youth can play in building a cohesive and harmonious society."),
  bodyPara("Awareness programmes conducted in villages and on campus have created a tangible impact on communities by spreading knowledge about environment conservation, health, hygiene, and family welfare. The off-campus activities, particularly Jatha visits and rally programmes, provided direct community exposure and fostered a deeper understanding of ground realities."),
  bodyPara("Campus activities through Shramadhan and celebration of national and international days have contributed to building a greener, more aware, and socially responsible college community. Each activity has reinforced the core values of the NSS: service, sacrifice, and selfless dedication to the betterment of society."),
  bodyPara("In conclusion, the NSS experience has been instrumental in shaping a well-rounded, socially conscious, and responsible individual. The skills, values, and perspectives gained through NSS will serve as a strong foundation for a lifetime of meaningful contribution to society and the nation."),
  pageBreak(),
];

// ─── REFERENCES ───────────────────────────────────────────────────────────────
const referencesPage = [
  sectionTitle("REFERENCES"),
  new Paragraph({ spacing: { before: 120, after: 120 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 80, after: 80 },
    indent: { left: 720, hanging: 360 },
    children: [new TextRun({ text: "[1] NSS Course Manual, Published by NSS Cell, VTU Belagavi.", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 80, after: 80 },
    indent: { left: 720, hanging: 360 },
    children: [new TextRun({ text: "[2] Government of Karnataka, NSS Cell, Activities Reports and its Manual.", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 80, after: 80 },
    indent: { left: 720, hanging: 360 },
    children: [new TextRun({ text: "[3] Government of India, NSS Cell, Activities Reports and its Manual.", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 80, after: 80 },
    indent: { left: 720, hanging: 360 },
    children: [new TextRun({ text: "[4] Ministry of Youth Affairs and Sports, Government of India. (2025). NSS Guidelines. New Delhi.", size: 24, font: "Times New Roman" })]
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 360, before: 80, after: 80 },
    indent: { left: 720, hanging: 360 },
    children: [new TextRun({ text: "[5] National Disaster Management Authority (NDMA), Government of India. (2025). Disaster Management Guidelines. New Delhi.", size: 24, font: "Times New Roman" })]
  }),
];

// ─── ASSEMBLE DOCUMENT ────────────────────────────────────────────────────────
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Times New Roman", size: 24 } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Times New Roman" },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Times New Roman" },
        paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 1 }
      },
    ]
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 2160 } // 1.5" left, 1" others
        }
      },
      children: [
        ...coverPage,
        ...certificatePage,
        ...acknowledgementPage,
        ...abstractPage,
        ...tocPage,
        ...listOfFigures,
        ...listOfTables,
        ...listOfAbbreviations,
        ...module1,
        ...module2,
        ...module3,
        ...module4,
        ...module5,
        ...conclusionPage,
        ...referencesPage,
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('/mnt/user-data/outputs/NSS-Sushanth_4th_Sem_.docx', buffer);
  console.log('Done!');
});