<?xml version="1.0" encoding="UTF-8"?> 
<!--
XSL file to transform an AFMS XML report into HTML.

Copyright 2008 Achim Köhler

This file is part of AFMS.

AFMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 2 of the License,
or (at your option) any later version.

AFMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AFMS.  If not, see <http://www.gnu.org/licenses/>.
-->

<!-- $Id$ -->

<!--
Using Microsoft Windows and msxsl, try stgh. like
    msxsl afsample.xml afmsreport.xsl -o afsample.html
-->

<xsl:stylesheet version="1.0" 
    xmlns="http://www.macht-publik.de"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<xsl:output method="html" encoding="utf-8"/>  

<xsl:template match="/artefacts">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta content="text/xhtml; charset=UTF-8" http-equiv="content-type"/>
    <title>AFMS Report</title>
    <link rel="stylesheet" type="text/css" href="afmsreport.css"/>
    </head>
    <body>
    <xsl:call-template name="tableofcontent"/>
    
    <h1><a name="productinformation">Product information</a></h1>
    <xsl:apply-templates select="productinformation"/>
    
    <h1><a name="textsections">Text sections</a></h1>
    <xsl:apply-templates select="simplesection"/>
    
    <h1>Glossary</h1>
    <dl class="glossary">
    <xsl:apply-templates select="glossaryentry"/>
    </dl>
    
    <h1><a name="features">Features</a></h1>    
    <xsl:apply-templates select="feature"/>

    <h1><a name="requirements">Requirements</a></h1>    
    <xsl:apply-templates select="requirement"/>

    <h1><a name="usecases">Usecases</a></h1>
    <xsl:apply-templates select="usecase"/>

    </body>
    </html>
</xsl:template>


<xsl:template name="tableofcontent">
    <div class="tableofcontent">
    <h1>Table of Contents</h1>
    <h2><a href="#productinformation">Product information</a></h2>
    <h2><a href="#textsections">Text sections</a></h2> 
    <ul>
    <xsl:for-each select="simplesection">    
        <xsl:call-template name="toclink">
            <xsl:with-param name="title" select="title"/>
            <xsl:with-param name="prefix">SS</xsl:with-param>
            <xsl:with-param name="ID" select="@ID" />
        </xsl:call-template> 
    </xsl:for-each>
    </ul>
    <h2><a href="#glossary">Glossary</a></h2>
    <h2><a href="#features">Features</a></h2> 
    <ul>
    <xsl:for-each select="feature">   
        <xsl:call-template name="toclink">
            <xsl:with-param name="title" select="title"/>
            <xsl:with-param name="prefix">FT</xsl:with-param>
            <xsl:with-param name="ID" select="@ID" />
        </xsl:call-template> 
    </xsl:for-each>
    </ul>
    <h2><a href="#requirements">Requirements</a></h2> 
    <ul>
    <xsl:for-each select="requirement">   
        <xsl:call-template name="toclink">
            <xsl:with-param name="title" select="title"/>
            <xsl:with-param name="prefix">REQ</xsl:with-param>
            <xsl:with-param name="ID" select="@ID" />
        </xsl:call-template> 
    </xsl:for-each>
    </ul>
    <h2><a href="#usecases">Usecases</a></h2>
    <ul>
    <xsl:for-each select="usecase">
        <xsl:call-template name="toclink">
            <xsl:with-param name="title" select="title"/>
            <xsl:with-param name="prefix">UC</xsl:with-param>
            <xsl:with-param name="ID" select="@ID" />
        </xsl:call-template>
    </xsl:for-each>
    </ul>

    </div>
</xsl:template>


<xsl:template name="toclink">
    <xsl:param name="title" />
    <xsl:param name="prefix" />
    <xsl:param name="ID" />
    <li>
        <a>
            <xsl:attribute name="href">#<xsl:value-of select="$prefix" />-<xsl:value-of select='format-number($ID, "000")'/></xsl:attribute>
            <xsl:value-of select="$prefix" />-<xsl:value-of select='format-number($ID, "000")'/>:
            <xsl:value-of select="$title"/>
        </a>
    </li>
</xsl:template>


<xsl:template name="artefactheadline">
    <xsl:param name="title" />
    <xsl:param name="prefix" />
    <a>
        <xsl:attribute name="name">
        <xsl:value-of select="$prefix" />-<xsl:value-of select='format-number(@ID, "000")'/>
        </xsl:attribute>        
        <xsl:value-of select="$prefix" />-<xsl:value-of select='format-number(@ID, "000")'/>:        
        <xsl:value-of select="$title"/>
    </a>
</xsl:template>


<xsl:template match="productinformation">
    <div class="productinfo">
        <div class="producttitle"><xsl:value-of select="title"/></div>
        <xsl:copy-of select="description" />
    </div>
</xsl:template>


<xsl:template match="simplesection">
    <div class="simplesection">
    <h2>
        <xsl:call-template name="artefactheadline">
            <xsl:with-param name="title" select="title"/>
            <xsl:with-param name="prefix">SS</xsl:with-param> 
        </xsl:call-template> 
    </h2>
    <xsl:copy-of select="content" />
    </div>
</xsl:template>


<xsl:template match="glossaryentry">
    <dt>
        <p class="glossaryid">[GE-<xsl:value-of select='format-number(@ID, "000")'/>]</p>
        <p class="glossarytitle">
            <span class="glossarytitle"><xsl:value-of select="title"/></span>
        </p>
    </dt>
    <dd>
        <div class="glossarydescription">
            <xsl:copy-of select="description" />
        </div>
    </dd>
</xsl:template>


<xsl:template name="relatedusecases">
    <tr class="aftable">
        <th class="aftable">
            Related usecases
        </th>
        <td class="aftable">
        <ul>
            <xsl:for-each select="relatedusecases/ID">
            <xsl:variable name = "ID" ><xsl:value-of select="normalize-space(.)"/></xsl:variable>
            <xsl:call-template name="toclink">
                <xsl:with-param name="title" select="/artefacts/usecase[@ID=$ID]/title"/>
                <xsl:with-param name="prefix">UC</xsl:with-param>
                <xsl:with-param name="ID" select="$ID" />
            </xsl:call-template>
            </xsl:for-each>
        </ul>
        </td>
    </tr>
</xsl:template>


<xsl:template name="relatedtestcases">
    <tr class="aftable">
        <th class="aftable">
            Related testcases
        </th>
        <td class="aftable">
        <ul>
            <xsl:for-each select="relatedtestcases/ID">
            <xsl:variable name = "ID" ><xsl:value-of select="normalize-space(.)"/></xsl:variable>
            <xsl:call-template name="toclink">
                <xsl:with-param name="title" select="/artefacts/testcase[@ID=$ID]/title"/>
                <xsl:with-param name="prefix">TC</xsl:with-param>
                <xsl:with-param name="ID" select="$ID" />
            </xsl:call-template>
            </xsl:for-each>
        </ul>
        </td>
    </tr>
</xsl:template>


<xsl:template name="relatedfeatures">
    <tr class="aftable">
        <th class="aftable">
            Related features
        </th>
        <td class="aftable">
        <ul>
            <xsl:for-each select="relatedfeatures/ID">
            <xsl:variable name = "ID" ><xsl:value-of select="normalize-space(.)"/></xsl:variable>
            <xsl:call-template name="toclink">
                <xsl:with-param name="title" select="/artefacts/feature[@ID=$ID]/title"/>
                <xsl:with-param name="prefix">FT</xsl:with-param>
                <xsl:with-param name="ID" select="$ID" />
            </xsl:call-template>
            </xsl:for-each>
        </ul>
        </td>
    </tr>
</xsl:template>


<xsl:template name="relatedrequirements">
    <tr class="aftable">
        <th class="aftable">
            Related requirements
        </th>
        <td class="aftable">
        <ul>
            <xsl:for-each select="relatedrequirements/ID">
            <xsl:variable name = "ID" ><xsl:value-of select="normalize-space(.)"/></xsl:variable>
            <xsl:call-template name="toclink">
                <xsl:with-param name="title" select="/artefacts/requirement[@ID=$ID]/title"/>
                <xsl:with-param name="prefix">REQ</xsl:with-param>
                <xsl:with-param name="ID" select="$ID" />
            </xsl:call-template>
            </xsl:for-each>
        </ul>
        </td>
    </tr>    
</xsl:template>


<xsl:template match="feature">
    <div class="feature">
        <h2>
            <xsl:call-template name="artefactheadline">
                <xsl:with-param name="title" select="title"/>
                <xsl:with-param name="prefix">FT</xsl:with-param>
            </xsl:call-template>
        </h2>
        <table class="aftable">
            <tr class="aftable">
                <th class="aftable">
                    Description
                </th>
                <td class="aftable">
                <xsl:copy-of select="description" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Priority
                </th>
                <td class="aftable">
                <xsl:value-of select="priority" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Status
                </th>
                <td class="aftable">
                <xsl:value-of select="status" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Key
                </th>
                <td class="aftable">
                <xsl:value-of select="version" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Risk
                </th>
                <td class="aftable">
                <xsl:value-of select="risk" />
                </td>
            </tr>
            <xsl:call-template name="relatedrequirements" />
            <xsl:call-template name="relatedusecases" />
        </table>
    </div>
</xsl:template>

<xsl:template match="requirement">
    <div class="requirement">
        <h2>
            <xsl:call-template name="artefactheadline">
                <xsl:with-param name="title" select="title"/>
                <xsl:with-param name="prefix">REQ</xsl:with-param> 
            </xsl:call-template> 
        </h2>
        <table class="aftable">
            <tr class="aftable">
                <th class="aftable">
                    Description
                </th>
                <td class="aftable">
                <xsl:copy-of select="description" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Priority
                </th>
                <td class="aftable">
                <xsl:value-of select="priority" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Key
                </th>
                <td class="aftable">
                <xsl:value-of select="version" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Complexity
                </th>
                <td class="aftable">
                <xsl:value-of select="complexity" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Assigned
                </th>
                <td class="aftable">
                <xsl:value-of select="assigned" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Effort
                </th>
                <td class="aftable">
                <xsl:value-of select="effort" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Category
                </th>
                <td class="aftable">
                <xsl:value-of select="category" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Origin
                </th>
                <td class="aftable">
                <xsl:copy-of select="origin" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Rationale
                </th>
                <td class="aftable">
                <xsl:value-of select="rationale" />
                </td>
            </tr>
            <xsl:call-template name="relatedfeatures" />
            <xsl:call-template name="relatedrequirements" />
            <xsl:call-template name="relatedusecases" />
            <xsl:call-template name="relatedtestcases" />
        </table>
    </div>
</xsl:template>


<xsl:template match="usecase">
    <div class="usecase">
        <h2>
            <xsl:call-template name="artefactheadline">
                <xsl:with-param name="title" select="title"/>
                <xsl:with-param name="prefix">UC</xsl:with-param>
            </xsl:call-template>
        </h2>
        <table class="aftable">
            <tr class="aftable">
                <th class="aftable">
                    Priority
                </th>
                <td class="aftable">
                <xsl:value-of select="priority" />
                </td>
            </tr>
            <tr class="aftable">
                <th class="aftable">
                    Use frequency
                </th>
                <td class="aftable">
                <xsl:value-of select="usefrequency" />
                </td>
            </tr>

       </table>
    </div>
</xsl:template>
</xsl:stylesheet>
