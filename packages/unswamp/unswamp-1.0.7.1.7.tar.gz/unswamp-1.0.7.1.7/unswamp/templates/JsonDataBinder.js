"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.JsonDataBinder = void 0;
var $ = require("jquery");
var JsonDataBinder = /** @class */ (function () {
    function JsonDataBinder(data) {
        this.toc = [];
        this.max_level = 5;
        this.min_level = 4;
        this.data = data;
        this.docType = this.getRenderType(data);
        if (this.docType == RenderType.CheckSuite) {
            this.bindCheckSuite(data);
        }
    }
    JsonDataBinder.prototype.bindCheckSuite = function (data) {
        document.title = "Docs '" + data.id + "' CheckSuite";
        this.appendHeading(data.id, 3);
        this.bindInformation(data);
        this.bindTableChecks(data);
        this.bindColumnChecks(data);
        this.bindCustomChecks(data);
        this.bindToc(this.toc, this.max_level, this.min_level);
    };
    JsonDataBinder.prototype.bindInformation = function (data) {
        this.appendHeading("Information", 4);
        this.appendHeading("Check Suite", 5);
        var info = {
            "Id": data.id,
            "{un}swamp version": data._unswamp_version
        };
        var tbl = this.getKvpTable(info);
        this.appendMain(tbl);
        this.appendHeading("Meta Data", 5);
        tbl = this.getKvpTable(data.meta_data);
        this.appendMain(tbl);
    };
    JsonDataBinder.prototype.bindTableChecks = function (data) {
        var checks = data.checks.filter(function (c) { return c.level == "table"; });
        if (checks.length == 0) {
            return;
        }
        this.appendHeading("Table Checks", 4);
        checks = checks.sort(function (a, b) { return a.id > b.id ? 1 : -1; });
        this.appendColumnCheckAccordion(checks, "table_checks");
    };
    JsonDataBinder.prototype.bindColumnChecks = function (data) {
        var checks = data.checks.filter(function (c) { return c.level == "column"; });
        if (checks.length == 0) {
            return;
        }
        this.appendHeading("Column Level Checks", 4);
        checks = checks.sort(function (a, b) { return a.column_name > b.column_name ? 1 : -1; });
        var lastCol = "";
        var collChecks = [];
        for (var pos in checks) {
            var check = checks[pos];
            var currCol = check.column_name;
            if (lastCol != currCol) {
                if (lastCol != "") {
                    this.appendColumnCheckAccordion(collChecks, lastCol, true);
                    collChecks = [];
                }
                lastCol = currCol;
            }
            collChecks.push(check);
        }
        this.appendColumnCheckAccordion(collChecks, lastCol, true);
    };
    JsonDataBinder.prototype.bindCustomChecks = function (data) {
        var checks = data.checks.filter(function (c) { return c.level == "custom"; });
        if (checks.length == 0) {
            return;
        }
        this.appendHeading("Custom Checks", 4);
        checks = checks.sort(function (a, b) { return a.id > b.id ? 1 : -1; });
        this.appendColumnCheckAccordion(checks, "custom_checks");
    };
    JsonDataBinder.prototype.bindToc = function (toc, max_level, min_level) {
        var html = "";
        var last_level = 0;
        for (var pos in toc) {
            var val = toc[pos];
            if (val.level <= max_level && val.level >= min_level) {
                if (last_level < val.level) {
                    html += "<ul>";
                }
                else if (last_level > val.level) {
                    html += "</ul>";
                }
                html += '<li><a href="#' + val.id + '">' + val.heading + '</a></li>';
                last_level = val.level;
            }
        }
        html += "</ul>";
        $("#toc").append(html);
    };
    JsonDataBinder.prototype.getRenderType = function (data) {
        if (data.unswamp_type == "unswamp.objects.CheckSuite.CheckSuite") {
            return RenderType.CheckSuite;
        }
    };
    JsonDataBinder.prototype.appendMain = function (html) {
        $("#content_main").append(html);
    };
    JsonDataBinder.prototype.getJsonHtml = function (obj) {
        var obj_json = JSON.stringify(obj, null, 4).trim();
        return '<div class="code-box"><pre class="my-0"><code class="fw-lighter">' + obj_json + '</code></pre></div>';
    };
    JsonDataBinder.prototype.getKvpRow = function (key, value) {
        var tmp_val = value;
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            tmp_val = "{";
            for (var obj_key in value) {
                tmp_val += '"' + obj_key + '" : "' + value[obj_key] + '", ';
            }
            tmp_val += "}";
        }
        return '<tr><th scope="row">' + key + '</th><td>' + tmp_val + '</td></tr>';
    };
    JsonDataBinder.prototype.getKvpTable = function (items) {
        var html = '<table class="table table-striped table-sm table-bordered">';
        for (var key in items) {
            html += this.getKvpRow(key, items[key]);
        }
        html += '</table>';
        return html;
    };
    JsonDataBinder.prototype.getColumnCheckAccordion = function (checks, id_part) {
        var html = '<div class="accordion" id="accordionExample_' + id_part + '">';
        for (var pos in checks) {
            var check = checks[pos];
            var checkId = id_part + '_' + pos;
            html += '<div class="accordion-item">';
            html += '<h2 class="accordion-header" id="heading' + checkId + '">';
            html += '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse' + checkId + '" aria-expanded="false" aria-controls="collapse' + checkId + '">';
            this.getHeading(check.id, 5, 'heading' + checkId);
            html += check.id;
            html += '</button>';
            html += '</h2>';
            html += '<div id="collapse' + checkId + '" class="accordion-collapse collapse" aria-labelledby="heading' + checkId + '" data-bs-parent="#accordionExample_' + id_part + '">';
            html += '<div class="accordion-body">';
            html += this.getCheckContent(check);
            html += '</div>';
            html += '</div>';
            html += '</div>';
        }
        html += "</div>";
        return html;
    };
    JsonDataBinder.prototype.appendColumnCheckAccordion = function (colChecks, colName, heading) {
        if (heading === void 0) { heading = false; }
        var html = '<div class="py-2">';
        if (heading) {
            html += this.getHeading("Column " + colName, 5);
        }
        html += this.getColumnCheckAccordion(colChecks, colName);
        html += '</div>';
        this.appendMain(html);
    };
    JsonDataBinder.prototype.getCheckContent = function (check) {
        var info = {
            "Id": check.id,
            "Type": check.unswamp_type,
            "Description": check.description,
            "Details": "ToDo",
        };
        var html = this.getHeading("Information", 6);
        html += this.getKvpTable(info);
        html += this.getHeading("Meta Data", 6);
        html += this.getKvpTable(check.meta_data);
        html += this.getHeading("JSON", 6);
        html += this.getJsonHtml(check);
        return html;
    };
    JsonDataBinder.prototype.getHeading = function (heading, level, id) {
        if (id === void 0) { id = null; }
        var head_id = id;
        if (head_id == null) {
            head_id = this.getHeadId(heading);
        }
        this.toc.push({ "heading": heading, "level": level, "id": head_id });
        return '<h' + level + ' id="' + head_id + '">' + heading + '</h' + level + '>';
    };
    JsonDataBinder.prototype.getHeadId = function (heading) {
        var head_id = heading.toLowerCase();
        head_id = head_id.replace(" ", "");
        head_id = "heading_" + head_id;
        return head_id;
    };
    JsonDataBinder.prototype.appendHeading = function (heading, level) {
        heading = this.getHeading(heading, level);
        this.appendMain(heading);
    };
    return JsonDataBinder;
}());
exports.JsonDataBinder = JsonDataBinder;
var RenderType;
(function (RenderType) {
    RenderType[RenderType["Unknown"] = 0] = "Unknown";
    RenderType[RenderType["CheckSuite"] = 1] = "CheckSuite";
    RenderType[RenderType["CheckRun"] = 2] = "CheckRun";
})(RenderType || (RenderType = {}));
