import styles
Style = styles.Style()

BPMN_WIDTH = "820"

draw = {
  "bpmn_lanes" : {
    "Supplier": {
        "geometry":    f"y=20; width={BPMN_WIDTH}; height=120;",
        "blocks":{
            "Registration": 			"x=70",
            "Seting up integration":  	"x=270",
            "Setting up LPoints":		"x=470",
            "Get reports":				"x=670",
        }
    },

    "Logistic poins": {
        "geometry":    f'''y=140; width={BPMN_WIDTH}; height=120;''',
        "block_params":f'''{Style.GRAY};label=QR code;''',
        "blocks":{
            "Generate LEvent message":	"x=470",
        }
    },
     "Misos.LES": {
        "geometry":    f"y=260; width={BPMN_WIDTH}; height=170;",
        "lane_params":"",
        "block_params":f"{Style.BLUE};label=QMS.LES",
        "blocks": {
            "Manage Supplier":			"x=70;label=MDM;text=<br>(Scoring);fillColor=#ffe6cc",
            "Manage Logistic point":	"x=270;label=MDM",
            "Message processing":		"x=470;label=GATE",
            "LES BI & reports":			"x=670;label=BI",
            "Data Exchange & Delivery":	"x= 70; y=110; width=720; height=30;label=Bus",
        }
    },

    "Plant": {
        "geometry":    f"y=430; width={BPMN_WIDTH}; height=120;",
        "block_params":f"{Style.MAROON};label=Plant.LES;",
        "blocks": {
            "Supplier manage":			"x=70",
            "LES Exchange":				"x=470",
            "LES BI & Report":   		"x=670",
        }
    },
},

"connections" : [
    ["Registration"				, "Manage Supplier" 			, "company info"		,  Style.LINE_DEF],
    ["Manage Supplier"			, "Seting up integration" 		, "ACCESS_KEY"			,  Style.LINE_DEF],
    ["Seting up integration"	, "Manage Logistic point"		, "places, parts"		,  Style.LINE_DEF],
    ["Seting up integration"	, "Setting up LPoints" 			,"configure & coding"	,  Style.LINE_DEF],
    ["Setting up LPoints"		, "Generate LEvent message" 	,"equipment"			,  Style.LINE_DEF],
    ["Generate LEvent message"	, "Message processing"			,"LES data"				,  Style.LINE_LES],
    ["Message processing"		, "LES BI & reports"			,"LES data"				,  Style.LINE_LES],
    ["Get reports"				, "LES BI & reports"			,"LES reports"			,  Style.LINE_DEF],
    ["Message processing"		, "Data Exchange & Delivery"	,"AMQP"					,  Style.LINE_DOTTED],
    ["Manage Logistic point"	, "Data Exchange & Delivery"	,"AMQP"					,  Style.LINE_BUS],
    ["Manage Supplier"			, "Data Exchange & Delivery"	,"AMQP"					,  Style.LINE_BUS],
    ["Supplier manage"			, "Data Exchange & Delivery"	,"AMQP"					,  Style.LINE_BUS],
    ["LES Exchange"				, "Data Exchange & Delivery"	,"AMQP"					,  Style.LINE_BUS],
    ["LES BI & Report"			, "Data Exchange & Delivery"	,"AMQP"					,  Style.LINE_BUS],
    ]
}
