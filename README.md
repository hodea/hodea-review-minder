# hodea-review-minder
**Python 3 scripts to assist code reviews**

![logo](logo/hodea_review_minder_logo.png)

<table>
  <tr>
    <td>Homepage:</td>
    <td>http://www.hodea.org</td>
  </tr>
  <tr>
    <td>Source code:</td>
    <td>https://github.com/hodea/hodea-review-minder</td>
  </tr>
</table>

---

## Introduction

The hodea-review-minder is a collection of python 3 scripts which helps
to conduct code reviews.

The concept of the tool is that issues found during a code review are
directly written into the source code as a special C/C++ comment.
If an issue is solved it is marked as closed, or it is deleted from the
source code.

When the tool is invoked it:

- Parses the source code for new, updated, closed or rejected findings
- Maintains a database file with the review findings
- Generates a review report based on the database file

The configuration, the database file and the generated report is
usually kept within the project and checked into the version control
system.

The hodea-review-minder can be used for peer reviews as well as for
group reviews.

## Rational

There are two common approaches to keep track of review findings and
to document that the code has been reviewed.

1. Maintain the list of findings in a separate document using standard
   office tools, e.g. Microsoft World or Excel.
2. Use dedicated review tools, e.g. CodeCollaborator or gerrit.

Using office tools to document reviews and to keep track of findings is
cumbersome. You lose the connection to the source code. You can document
the file and line number for a finding at the time of the review. But
the source code usually changes and your review document gets outdated.

Dedicated review tools are complex and need support from the IT department.
They have their own database to hold snapshots of the source code and manage
review issues. The findings are stored somewhere outside the real source
code. The learning curve is high and it is easy for a software engineer to
ignore the findings.

After being having worked with both variants, the initiators of the
hodea-review-minder decided to look for a more practical approach.

We like to have the review comments directly within the source code for
several reasons:

- You can use your favorite IDE / editor to conduct the code review.
- You have the full context of a review finding.
- The review findings are under version control, together with the code.
- Developers are highly motivated to solve the issues to get the review
  comments out of their code.

## Configuration

The hodea-review-minder is called from the root directory of your project.

Let us assume that the review minder is installed in
/opt/hodea-review-minder, and your project is ~/work/foo.

When the review minder is called the first time, it generates a subdirectory
review_minder with the following files:

- minder.cfg
- minder.db


```sh
$ cd ~/work/foo
$ python3 /opt/hodea-review-minder/reviewminder.py
$ ls review_minder
minder.cfg  minder.db
```
*minder.cfg* is the configuration file and must be adapted for the project.
Follow the instructions within the comment for this purpose.

*minder.db* is the database file used to keep track of review findings.

## Review comments

Review comments can be directly added to the source code. The simplest
review comment is:

```c
/*TODO:review
This is a simple review comment.
*/
```

A more complex review comment is:

```c
/*TODO:review:new:severity:minor
This is a more complex review comment.
*/
```

## Parse source code and update the database

The following command parses the source code and updates the database file.

```sh
$python3 /opt/hodea-review-minder/reviewminder.py -r false
```

The script also updates the review comments within the source code. E.g.
if the review comment is new it assigns an *ID* to it.

For the example above the review comments are changed to:

```c
/*TODO:review:STATUS:open:undefined:RM_ID_0___ab44d952a85c1851b281cd3355be99205803f0f8
This is a simple review comment.
*/

/*TODO:review:STATUS:open:minor:RM_ID_1___8a6dcb262601b3b49a5be63b1cede36b7f2d686d
This is a more complex review comment.
*/
```

## Generate an HTML report

The following command generates the html report review_minder/miner.html.

```sh
$ python3 /opt/hodea-review-minder/reviewminder.py -r true
```

It can be views using a web browser:

```
$ firefox review_minder/minder.html
```

## Reviewing documents instead of source code

If you have to review documents rather than source code you can
write the findings into a text file (.txt) in the C/C++ comment
style shown above, and use hodea-review-minder to parse the text file.
