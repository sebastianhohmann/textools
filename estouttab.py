import re

class CleanEstout(object):

	'''
	Class to further clean up and format the output of
	of a call to Stata's estout.
	Can create single and multi-panel tables. 
	Important: make sure you feed in input string(s) as a list. 

	I.e. for a single panel, create an instance like so:
	ceo = CleanEstout([string_containing_table]). 

	For a multi panel table, write:
	tablist = [string_containing_t1,
			   string_containing_t2,
			   string_containing_t3]
	ceo = CleanEstout(tablist)
	'''

	def __init__(self, t):
		self.t = t

	def clean_tab_onepanel(self, caption="", label="", notes="",
				           rszbx=True, rszwidth=1, rmspace=True,
				           colnames=False, morelines=False):

		nt = self.t[0]

		nt = re.sub(r'\*\*\*&', r'$^{***}$&', nt)
		nt = re.sub(r'\*\* &', r'$^{**}$&', nt)
		nt = re.sub(r'\*  &', r'$^{*}$&', nt)
		nt = re.sub(r'\*\*\*\\', r'$^{***}$\\', nt)
		nt = re.sub(r'\*\* \\', r'$^{**}$\\', nt)
		nt = re.sub(r'\*  \\', r'$^{*}$\\', nt)


		nl = '[ht!]\n\\\\singlespacing\n\\\\centering'
		nt = re.sub(r'\[htbp\].+?\\fi}', nl, nt, flags = re.DOTALL)
		if rmspace:
			nt = re.sub(r'\[1em\]', '', nt, flags = re.DOTALL)


		l1 = '\\\\resizebox{%s\\\\columnwidth}{!}' % rszwidth
		l2 = '{%\n'
		nl = l1+l2
		nt = re.sub(r'(\\begin\{tabular)', r'%s\1' % nl, nt)

		if label:
			nl = "\n\\\\label{%s}" % label
			nt = re.sub(r'(\n\\resizebox)', r'%s\1' % nl, nt, flags = re.DOTALL)


		l1 = "}\n"
		l2a = "\\\\captionsetup{size=scriptsize, justification="
		l2b = "justified, width=%s\\\\columnwidth}\n" % rszwidth 
		l3 = "\\\\caption*{"
		l4 = notes
		l5 = "}\n"
		NL = l1+l2a+l2b+l3+l4+l5
		nt = re.sub(r'(\\end\{table)', r'%s\1' % NL, nt)

		if morelines:
			for line in morelines:
				nt = re.sub(r'(\n%s)' % line, r'\n\\hline\1', nt, flags = re.DOTALL)


		if colnames:
			pattern = '(\\\\multicolumn\\{1\\}\\{c\\}\\{\\([0-9]+\\)\\}\\\\\\\\\n)(.+?\n)'
			NL = ""
			for cn in colnames:
				NL += "&{}".format(cn)
			NL += "\\\\\\\\\n" 
			nt = re.sub(r'%s' % pattern, r"\1%s" % NL, nt, flags = re.DOTALL)

		return(nt)

	def clean_tab_multpanel(self, caption="", label="", notes="",
				            rszbx=True, rszwidth=1, rmspace=True):

		pass		