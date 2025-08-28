from warnings import warn
import polars as pl
import argparse
import os

# 默认的数学学院课程代码列表
DEFAULT_COURSE_CODES = [
    "AIS631003",
    "AIS631004",
    "DATA130008",
    "MATH120003",
    "MATH120004",
    "MATH120008",
    "MATH120009",
    "MATH120010",
    "MATH120011",
    "MATH120014",
    "MATH120014h",
    "MATH120015",
    "MATH120015h",
    "MATH120016",
    "MATH120017",
    "MATH120020",
    "MATH120021",
    "MATH120022",
    "MATH120044",
    "MATH130001",
    "MATH130002",
    "MATH130004",
    "MATH130005",
    "MATH130006",
    "MATH130006h",
    "MATH130007",
    "MATH130007h",
    "MATH130008",
    "MATH130009",
    "MATH130009h",
    "MATH130010",
    "MATH130011",
    "MATH130011h",
    "MATH130012",
    "MATH130012h",
    "MATH130013",
    "MATH130014",
    "MATH130015",
    "MATH130016",
    "MATH130017",
    "MATH130017h",
    "MATH130018",
    "MATH130019",
    "MATH130020",
    "MATH130021",
    "MATH130022",
    "MATH130024",
    "MATH130026",
    "MATH130027",
    "MATH130029",
    "MATH130030",
    "MATH130032",
    "MATH130033",
    "MATH130036",
    "MATH130037",
    "MATH130038",
    "MATH130039",
    "MATH130040",
    "MATH130041",
    "MATH130041h",
    "MATH130042",
    "MATH130043",
    "MATH130044",
    "MATH130047",
    "MATH130052",
    "MATH130055",
    "MATH130056",
    "MATH130057",
    "MATH130058",
    "MATH130059",
    "MATH130060",
    "MATH130061",
    "MATH130062",
    "MATH130063",
    "MATH130067",
    "MATH130068",
    "MATH130068h",
    "MATH130069",
    "MATH130070",
    "MATH130072",
    "MATH130073",
    "MATH130074",
    "MATH130075",
    "MATH130076",
    "MATH130077",
    "MATH130078",
    "MATH130080",
    "MATH130087",
    "MATH130088",
    "MATH130089",
    "MATH130090",
    "MATH130091",
    "MATH130092",
    "MATH130094",
    "MATH130095",
    "MATH130096",
    "MATH130097",
    "MATH130098",
    "MATH130099",
    "MATH130100",
    "MATH130101",
    "MATH130102",
    "MATH130103",
    "MATH130104",
    "MATH130105",
    "MATH130106",
    "MATH130107",
    "MATH130108",
    "MATH130109",
    "MATH130110",
    "MATH130111",
    "MATH130112",
    "MATH130112h",
    "MATH130113",
    "MATH130114",
    "MATH130115",
    "MATH130116",
    "MATH130117",
    "MATH130118",
    "MATH130119",
    "MATH130120",
    "MATH130121",
    "MATH130122",
    "MATH130123",
    "MATH130124",
    "MATH130125",
    "MATH130126",
    "MATH130127",
    "MATH130128",
    "MATH130129",
    "MATH130130",
    "MATH130131",
    "MATH130132",
    "MATH130133",
    "MATH130134",
    "MATH130135",
    "MATH130136",
    "MATH130137",
    "MATH130138",
    "MATH130139",
    "MATH130140h",
    "MATH130141",
    "MATH130142",
    "MATH130143h",
    "MATH130144h",
    "MATH130145h",
    "MATH130146",
    "MATH130147",
    "MATH130148",
    "MATH130149",
    "MATH130150",
    "MATH130151",
    "MATH130152",
    "MATH130153",
    "MATH130154",
    "MATH130155",
    "MATH130156",
    "MATH130157",
    "MATH130158",
    "MATH130159",
    "MATH130160",
    "MATH130161",
    "MATH130162",
    "MATH130163",
    "MATH130164h",
    "MATH130165h",
    "MATH130166",
    "MATH130167",
    "MATH130168",
    "MATH130169",
    "MATH130170",
    "MATH130171  ",
    "MATH130172  ",
    "MATH130173  ",
    "MATH130174  ",
    "MATH130175  ",
    "MATH130177 ",
    "MATH130178 ",
    "MATH130179 ",
    "MATH130180 ",
    "MATH130181 ",
    "MATH130182",
    "MATH130183",
    "MATH130184",
    "MATH130185",
    "MATH130186",
    "MATH130186h",
    "MATH130187",
    "MATH130188",
    "MATH130189",
    "MATH130190",
    "MATH130191",
    "MATH130193",
    "MATH130194h",
    "MATH130195h",
    "MATH130196h",
    "MECH130084",
    "PHYS120001",
    "PHYS120002",
    "PHYS120013",
    "PHYS120014",
    "PHYS120016",
    "PHYS120016h",
    "PHYS120017",
    "PHYS120017h",
    "PHYS120018",
    "PHYS120018h",
    "PHYS130008",
    "MATH20004",
    "MATH30002",
    "MATH30001",
    "STAT30013",
    "STAT30012",
    "MATH40001",
    "MATH40002",
    "MATH40006",
    "MATH50008",
    "MATH50001",
    "MATH50002",
    "MATH50007",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--course_list",
        "-c",
        type=str,
        required=False,
        default=None,
        help="课程列表文件路径 (可选，如果未提供，则使用内置的数学学院课程列表)",
    )
    parser.add_argument(
        "--grades",
        "-g",
        type=str,
        required=True,
        help="成绩文件路径",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=False,
        default="output.csv",
        help="输出文件名，默认是output.csv",
    )
    parser.add_argument(
        "--year",
        "-y",
        type=str,
        required=False,
        default=None,
        help="要计算绩点的学年，默认是所有学年",
    )
    args = parser.parse_args()

    dir_to_grades = os.path.dirname(args.grades)

    # 获取课程代码列表
    if args.course_list:
        # 使用用户提供的课程列表文件
        try:
            course_list = pl.read_csv(args.course_list)
            course_codes = course_list["课程代码"].to_list()
        except Exception as e:
            raise Exception(f"读取课程列表文件失败: {e}")
    else:
        # 使用内置的默认课程列表
        course_codes = DEFAULT_COURSE_CODES

    try:
        grades = pl.read_csv(args.grades).with_columns(
            (pl.col("学分") * pl.col("绩点")).alias("学分绩")
        )
    except Exception as e:
        raise Exception(f"读取成绩文件失败: {e}")

    grades_copy = grades.clone()

    if args.year is not None:
        grades = grades.filter(pl.col("学年学期").str.contains(args.year))

    if grades.is_empty():
        raise Exception("给定学年没有找到任何课程，请检查学年是否正确")

    if grades["学号"].n_unique() < grades_copy["学号"].n_unique():
        # 筛选出grades_copy中有的但是grades中没有的人名
        all_students = grades_copy.select(["学号", "姓名"]).unique()
        filtered_students = grades.select(["学号", "姓名"]).unique()
        missing_students = all_students.join(
            filtered_students, on=["学号", "姓名"], how="anti"
        )
        if missing_students.height > 0:
            warn(
                "Warning: 有些学生在指定学年没有修读任何课程，名单已经保存到missing_grades.csv文件中"
            )
            missing_students.write_csv(
                os.path.join(dir_to_grades, "missing_grades.csv")
            )

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
    ).write_csv(os.path.join(dir_to_grades, args.output))


if __name__ == "__main__":
    main()
