/**
 * Created by jinyan on 11/04/2017.
 */
var surveyJSON = {
    pages: [
        {
            elements: [
                {
                    type: "text",
                    inputType: "date",
                    name: "date",
                    title: "Date"
                },
                {
                    type: "text",
                    inputType: "time",
                    name: "time",
                    title: "Time"
                },
                {
                    type: "dropdown",
                    choices: [
                        {
                            value: "1",
                            text: "Light"
                        },
                        {
                            value: "2",
                            text: "Circle"
                        },
                        {
                            value: "3",
                            text: "Triangle"
                        },
                        {
                            value: "4",
                            text: "Fireball"
                        },
                        {
                            value: "5",
                            text: "Sphere"
                        },
                        {
                            value: "6",
                            text: "Disk"
                        },
                        {
                            value: "7",
                            text: "Oval"
                        },
                        {
                            value: "8",
                            text: "Formation"
                        },
                        {
                            value: "9",
                            text: "Changing"
                        },
                        {
                            value: "10",
                            text: "Cigar"
                        },
                        {
                            value: "11",
                            text: "Flash"
                        },
                        {
                            value: "12",
                            text: "Rectangle"
                        },
                        {
                            value: "13",
                            text: "Cylinder"
                        },
                        {
                            value: "14",
                            text: "Diamond"
                        },
                        {
                            value: "15",
                            text: "Chevron"
                        },
                        {
                            value: "16",
                            text: "Teardrop"
                        },
                        {
                            value: "17",
                            text: "Egg"
                        },
                        {
                            value: "18",
                            text: "Cone"
                        },
                        {
                            value: "19",
                            text: "Cross"
                        },
                        {
                            value: "20",
                            text: "Unknown"
                        }
                    ],
                    name: "shape",
                    title: "Shape"
                },
                {
                    type: "text",
                    name: "summary",
                    title: "Summary"
                },
                {
                    type: "text",
                    name: "city",
                    title: "City"
                },
                {
                    type: "dropdown",
                    choices: [
                        {
                            value: "1",
                            text: "AL"
                        },
                        {
                            value: "2",
                            text: "AK"
                        },
                        {
                            value: "3",
                            text: "AZ"
                        },
                        {
                            value: "4",
                            text: "AR"
                        },
                        {
                            value: "5",
                            text: "CA"
                        },
                        {
                            value: "6",
                            text: "CO"
                        },
                        {
                            value: "7",
                            text: "CT"
                        },
                        {
                            value: "8",
                            text: "DE"
                        },
                        {
                            value: "9",
                            text: "FL"
                        },
                        {
                            value: "10",
                            text: "GA"
                        },
                        {
                            value: "11",
                            text: "HI"
                        },
                        {
                            value: "12",
                            text: "ID"
                        },
                        {
                            value: "13",
                            text: "IL"
                        },
                        {
                            value: "14",
                            text: "IA"
                        },
                        {
                            value: "15",
                            text: "KS"
                        },
                        {
                            value: "16",
                            text: "KY"
                        },
                        {
                            value: "17",
                            text: "LA"
                        },
                        {
                            value: "18",
                            text: "ME"
                        },
                        {
                            value: "19",
                            text: "MD"
                        },
                        {
                            value: "20",
                            text: "MA"
                        },
                        {
                            value: "21",
                            text: "MI"
                        },
                        {
                            value: "22",
                            text: "MN"
                        },
                        {
                            value: "23",
                            text: "MS"
                        },
                        {
                            value: "24",
                            text: "MO"
                        },
                        {
                            value: "25",
                            text: "MT"
                        },
                        {
                            value: "26",
                            text: "NE"
                        },
                        {
                            value: "27",
                            text: "NV"
                        },
                        {
                            value: "28",
                            text: "NH"
                        },
                        {
                            value: "29",
                            text: "NJ"
                        },
                        {
                            value: "30",
                            text: "NM"
                        },
                        {
                            value: "31",
                            text: "NY"
                        },
                        {
                            value: "32",
                            text: "NC"
                        },
                        {
                            value: "33",
                            text: "ND"
                        },
                        {
                            value: "34",
                            text: "OH"
                        },
                        {
                            value: "35",
                            text: "OK"
                        },
                        {
                            value: "36",
                            text: "OR"
                        },
                        {
                            value: "37",
                            text: "PA"
                        },
                        {
                            value: "38",
                            text: "RI"
                        },
                        {
                            value: "39",
                            text: "SC"
                        },
                        {
                            value: "40",
                            text: "SD"
                        },
                        {
                            value: "41",
                            text: "TN"
                        },
                        {
                            value: "42",
                            text: "TX"
                        },
                        {
                            value: "43",
                            text: "UT"
                        },
                        {
                            value: "44",
                            text: "VT"
                        },
                        {
                            value: "45",
                            text: "VA"
                        },
                        {
                            value: "46",
                            text: "WA"
                        },
                        {
                            value: "47",
                            text: "WV"
                        },
                        {
                            value: "48",
                            text: "WI"
                        },
                        {
                            value: "49",
                            text: "WY"
                        },
                        {
                            value: "50",
                            text: "DC"
                        }
                    ],
                    name: "state",
                    title: "State"
                }
            ],
            name: "report"
        }
    ],
        title: "my report"
};

Survey.defaultBootstrapCss.navigationButton = "btn";
Survey.Survey.cssType = "bootstrap";
var survey = new Survey.Model(surveyJSON);
$("surveyContainer").Survey({
    model:survey
});