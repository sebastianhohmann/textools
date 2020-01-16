# Python class to convert .tex documents that contain
# - various package imports
# - tables 
# - figures
# into "barebones" documents that can be compiled with SW.
# Given a document converted to SW using the class, the class
# can convert back to the original .tex.

# For the "to SW" functionality,
# the class comments out all existing package imports
# and inserts only basic ones useable by SW. 
# It also comments out all table and figure imports
# and replaces them with placeholder tables and figures
# consisting only of table and figure environments, captions
# and labels. 

# Given a .tex document that is turned into a SW compatible 
# document using the class, the class can also reverse the changes
# removing all dummy tables and figures and removing
# the originally inserted comments around package imports, tables
# and figures that trip up SW

# (c) 2019, Sebastian Hohmann

import re

class SWRawtex(object):

	def __init__(self, inpath):
		self.inpath = inpath
		self.outpath = inpath[:-4] + "_notabfigforSW.tex"
		self.outpath2 = inpath[:-4] + "_forTEX.tex"
		self.read_data()

	def read_data(self):
		f = open(self.inpath, 'r')
		self.text = f.read()
		f.close()

	def pt(self):
		print(self.text)

	# method for commenting out blocks
	# to be able to use this inside an re.sub(), 
	# I am making this a static method for now
	# may want to revisit later
	# check also here
	# https://julien.danjou.info/guide-python-static-class-abstract-methods/
	@staticmethod
	def commentblock(match):
		out = ""
		xcut = match.group(1)
		for xl in xcut.split("\n"):
			if xl != "":
				out += "% " + "SWCOMMENT " + xl + "\n"
			else:
				out += xl + "\n"
		return(out) 

	@staticmethod
	def dummytable(match):
		out = match.group(1)
		if "% % SWCOMMENT" in out:
			return(out)
		else:
			path = re.search(r"input{(.+?)}", out).group(1)
			f = open(path, "r")
			txt = f.read()
			f.close()
			nl0A = "% " + "FORSWSTART\n"
			nl1 = "\\begin{table}[ht!]\n\\centering\n"
			nl2 = "\\caption{" + re.search(r"\\caption{(.+?)}", txt).group(1) + "}" + "\n"
			nl3 = "\\label{" + re.search(r"\\label{(.+?)}", txt).group(1) + "}" + "\n"
			nl4 = "\\begin{tabular}{c}\n"
			nl5 = "\\hline\nSOME TABLE CONTENT \\\\\n\\hline\n"
			nl6 = "\\end{tabular}\n"
			nl7 = "\\end{table}\n"
			nl0B = "% " + "FORSWEND\n"
			NL = nl0A+nl1+nl2+nl3+nl4+nl5+nl6+nl7+nl0B
			out += "\n" + NL
			return(out)

	@staticmethod
	def dummyfigure(match):
		out = match.group(1)
		# print(out)
		# if re.match(r"%\s%\sSWCOMMENT", out):
		# 	return(out)
		if "% SWCOMMENT %" in out:
			return(out)
		else:
			nl0A = "% " + "FORSWSTART\n"
			nl1 = "\\begin{figure}[ht!]\n\\centering\n"
			nl2 = "\\caption{" + re.search(r"\\caption{(.+?)}", out).group(1) + "}" + "\n"
			nl3 = "\\label{" + re.search(r"\\label{(.+?)}", out).group(1) + "}" + "\n"
			nl4 = "\\fbox{SOME FIGURE CONTENT}\n"
			nl5 = "\\end{figure}\n"
			nl0B = "% " + "FORSWEND\n"
			NL = nl0A+nl1+nl2+nl3+nl4+nl5+nl0B
			out += "\n" + NL
			out = out.replace("\\\\", "\\")	
			return(out)


	def tosw(self):
		t = self.text
		# commenting out the existing package imports
		t = re.sub(r"(\\usepackage.+)\\begin{document}", self.commentblock, t, flags = re.DOTALL)
		t = re.sub(r"\\title{", r"\\input{tcilatex}\n\\begin{document}\n\\title{", t, flags=re.DOTALL)

		# adding basic package imports to be understood by SW
		nl0A = "% " + "FORSWSTART\n"
		nl1 = "\\\\usepackage[left=3cm,top=2cm,right=3cm,bottom=2cm]{geometry}\n"
		nl2 = "\\\\usepackage{amsmath}\n"
		nl3 = "\\\\usepackage{amssymb}\n"
		nl4 = "\\\\usepackage[labelfont={bf}]{caption}\n"
		nl5 = "\\\\usepackage{setspace}\n"
		nl6 = "\\\\usepackage{natbib}\n"
		nl0B = "% " + "FORSWEND\n\n\n" 
		NL = nl0A+nl1+nl2+nl3+nl4+nl5+nl6
		t = re.sub(r"(\\input{tcilatex}\n)", r"%s\1%s" % (NL, nl0B), t, flags=re.DOTALL)

		# replacing figures with commented versions
		t = re.sub(r"(\\begin{figure.+?\\end{figure})", self.commentblock, t, flags = re.DOTALL)

		# replacing table imports with commented versions
		t = re.sub(r"(\\input{.+/)", r"% SWCOMMENT \1", t)

		# creating dummy versions of tables
		t = re.sub(r"(%.+SWCOMMENT\s\\input{.+?})", self.dummytable, t)

		# creating dummy versions of figures
		t = re.sub(r"(%\sSWCOMMENT\s\\begin{figure}.+?\\end{figure})", self.dummyfigure, t, flags = re.DOTALL)

		# removing within-section commenting
		t = re.sub(r"(\\counterwithin.+\\counterwithin.+?{section})", self.commentblock, t, flags = re.DOTALL)

		self.text = t

		f = open(self.outpath, 'w')
		f.write(self.text)
		f.close()


	def totex(self):
		t = self.text

		# getting rid of the dummy tables, figures, and barebones package imports
		t = re.sub(r"%\sFORSWSTART.+?%\sFORSWEND", "", t, flags = re.DOTALL)

		# removing the comments around the original tables, figures, and package imports
		t = re.sub(r"%\sSWCOMMENT\s", "", t)		

		self.text = t

		f = open(self.outpath2, 'w')
		f.write(self.text)
		f.close()


if __name__ == '__main__':
    swr = SWRawtex('./IM_ethrelig_August12.tex')
    swr.tosw()
    swr.totex()
    swr.pt()





