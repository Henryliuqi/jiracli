# -*- coding: utf-8 -*-
# This script is to generate the verison based reports

import argparse


class MyTeam(object):
	"""docstring for MyTeam"""
	def __init__(self, arg):
		super(MyTeam, self).__init__()
		self.arg = arg


def _read_options():
	# Build arg parser.
	parser = argparse.ArgumentParser(
				formatter_class=argparse.RawDescriptionHelpFormatter,
				description="Create Weekly report for specified assigned. Get the Markdown report feom repoet.md and get the html report from report.html. You can copy the html report into onenote as basis of the weekly report")
	# Options
	parser.add_argument("-u", "--unresolved", action="store_true", default=False, help="Whether to list unresolved tickets to this report but not limited to the update time.")
    parser.add_argument("-e", "--excel", action="store", default="", help="After the generation of report. Excel file will be created. However, some tickets make no sense in report you may want to ignore it. You can open the excel and change the visible column value to other value but not NA. Then you can specify the excel file and the report html file will be regenerated.")
    parser.add_argument("-s", "--sorter", action="append", default=[], help="It tell how to sort the report in html. Several fields are supported, npi, version, priority, assignee, status.  To specify multiple level of sorters,  use multile -s.  Example, -s npi -s version -s status. Note here this is the default sort sequence.")
    parser.add_argument("-v", "--versions", action="append", default=[], help="Specify the version the report cares.  For example, -v 2.4.0, you only care JIRA ticket with fix version with 2.4.0 inside. You can specify multiple verison tags like -s 2.2.0 -s 2.3.0 -s 2.4.0. These conditions will be ORed. If not specified,  JQL won't take the version  as part of search condition")
    parser.add_argument("-d", "--update", action="store", default="1w", help="w means week. d means day.  Assign a value that this will checked tickets assigned to you and it is updated >= the update time specified by you. The default value is 1w, which means in the past week. Example, -d 1d,  -d 3w")
    parser.add_argument("-a", "--assignees", action="store", default="nxa16738, nxa07168, nxa34233, nxa33892, nxa32595, nxa07599, nxa32306, nxf10088, nxa17969, nxa13122, nxa31034, nxa32755, nxa17403, nxa07631, nxa06981, nxf24241,nxf08061, nxf36200", metavar='', help="Assignees of the team to be calculater. It is combined by ',' and it use the core id as identifier. For example, b36089,b12345")

    return parser.parse_args()

if __name__ == '__main__':

	args = _read_options()
		