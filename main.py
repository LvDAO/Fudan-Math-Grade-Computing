import polars as pl
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--course_list",
        "-c",
        type=str,
        required=True,
        help="Path to the course list file",
    )
    parser.add_argument(
        "--grades",
        "-g",
        type=str,
        required=True,
        help="Path to the grades file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=False,
        default="output.csv",
        help="Path to the output file",
    )
    args = parser.parse_args()

    try:
        course_list = pl.read_csv(args.course_list)
    except Exception as e:
        print(f"Error reading course list file: {e}")
        return

    try:
        grades = pl.read_csv(args.grades).with_columns(
            (pl.col("学分") * pl.col("绩点")).alias("学分绩")
        )
    except Exception as e:
        print(f"Error reading grades file: {e}")
        return

    try:
        course_codes = course_list["课程代码"].to_list()
    except Exception as e:
        print(f"Error getting course codes: {e}")
        return

    math_grade_list = (
        grades.filter(
            (pl.col("最终成绩") != "P")
            & (pl.col("最终成绩") != "NP")
            & (pl.col("最终成绩") != "缓考")
            & (pl.col("课程序号").str.split(".").list.first().is_in(course_codes))
        )
        .group_by(["学号", "姓名"])
        .agg(
            [
                pl.col("学分绩").sum().alias("总专业学分绩"),
                pl.col("学分").sum().alias("总专业学分"),
            ]
        )
        .with_columns((pl.col("总专业学分绩") / pl.col("总专业学分")).alias("专业绩点"))
    )

    math_grade_list.write_csv(args.output)

    all_grade_list = (
        grades.filter(
            (pl.col("最终成绩") != "P")
            & (pl.col("最终成绩") != "NP")
            & (pl.col("最终成绩") != "缓考")
        )
        .group_by(["学号", "姓名"])
        .agg(
            [
                pl.col("学分绩").sum().alias("总学分绩"),
                pl.col("学分").sum().alias("总学分"),
            ]
        )
        .with_columns((pl.col("总学分绩") / pl.col("总学分")).alias("总绩点"))
    )

    person_grades = math_grade_list.select(["学号", "姓名", "专业绩点"]).join(
        all_grade_list.select(["学号", "姓名", "总绩点"]),
        on=["学号", "姓名"],
        how="left",
    )
    del all_grade_list, math_grade_list

    all_points = (
        grades.filter((pl.col("最终成绩") != "F") & (pl.col("最终成绩") != "NP"))
        .group_by(["学号", "姓名"])
        .agg(
            [
                pl.col("学分").sum().alias("总学分"),
            ]
        )
    )

    person_grades.join(all_points, on=["学号", "姓名"], how="left").sort(
        "总绩点", descending=True
    ).write_csv(args.output)


if __name__ == "__main__":
    main()
