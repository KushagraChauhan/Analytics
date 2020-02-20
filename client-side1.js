
<!– THREE STEPS TO INSTALL BROWSER PROPERTIES:

  1.  Copy the coding into the HEAD of your HTML document
  2.  Add the onLoad event handler into the BODY tag
  3.  Put the last coding into the BODY of your HTML document  –>

<!– STEP ONE: Paste this code into the HEAD of your HTML document  –>

<SCRIPT LANGUAGE=”JavaScript”>


<!– This script and many more are available free online at –>

<!– The JavaScript Source!! http://www.javascriptsource.com –>

<!– begin
function display() {
window.onerror=null;

colors = window.screen.colorDepth;
document.form.color.value = Math.pow (2, colors);
if (window.screen.fontSmoothingEnabled == true)
document.form.fonts.value = “Yes”;
else document.form.fonts.value = “No”;

document.form.navigator.value = navigator.appName;
document.form.version.value = navigator.appVersion;
document.form.colordepth.value = window.screen.colorDepth;
document.form.width.value = window.screen.width;
document.form.height.value = window.screen.height;
document.form.maxwidth.value = window.screen.availWidth;
document.form.maxheight.value = window.screen.availHeight;
document.form.codename.value = navigator.appCodeName;
document.form.platform.value = navigator.platform;
if (navigator.javaEnabled() 

<!– STEP THREE: Copy this code into the BODY of your HTML document  –>

<center>
<form name=form>
<table border=1 width=300>

<tr>
<td>current resolution:</td>
<td align=center><input type=text size=4 maxlength=4 name=width>
x <input type=text size=4 maxlength=4 name=height></td>
</tr>

<tr>
<td>
browser:</td>
<td align=center><input type=text size=20 maxlength=20 name=navigator></td>
</tr>
<tr>
<td>
max resolution:</td>
<td align=center><input type=text size=4 maxlength=4 name=maxwidth>
x <input type=text size=4 maxlength=4 name=maxheight></td>
</tr>

<tr>
<td>
version:</td>
<td align=center><input type=text size=20 maxlength=20 name=version></td>
</tr>

<tr>
<td>
color depth:</td>
<td align=center><input type=text size=2 maxlength=2 name=colordepth> bit</td>
</tr>

<tr>
<td>
code name:</td>
<td align=center><input type=text size=15 maxlength=15 name=codename></td>
</tr>

<tr>
<td>
platform:</td>
<td align=center><input type=text size=15 maxlength=15 name=platform></td>
</tr>

<tr>
<td>
colors:</td>
<td align=center><input type=text size=8 maxlength=8 name=color></td>
</tr>

<tr>
<td>
java enabled:</td>
<td align=center><input type=text size=3 maxlength=3 name=java></td>
</tr>

<tr>
<td>
anti-aliasing fonts:</td>
<td align=center><input type=text size=3 maxlength=3 name=fonts></td>
</tr>

<tr>
<td colspan=2 align=center>
<input type=button name=again value=”again?” onclick=”display()”></td>
</tr>
</table>
</form>
</center>

<p><center>
<font face=”arial, helvetica” size=”-2″>Free JavaScripts provided<br>
by <a href=”https://javascriptsource.com”>The JavaScript Source</a></font>
</center><p>

<!– Script Size:  3.31 KB –>
