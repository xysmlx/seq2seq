#encoding=utf-8

import os
import sys
import codecs
import click
import shutil
import make_seq2seq_data

@click.group()
def cli():
  pass

@click.command()
@click.argument("ques_path")
@click.argument("infer_path")
@click.argument("ques_done_path")
@click.argument("infer_done_path")
def store_done_ques(ques_path, infer_path, ques_done_path, infer_done_path):
  lines = codecs.open(ques_path, "r", "utf-8").readlines()
  infer_lines = codecs.open(infer_path, "r", "utf-8").readlines()
  assert  len(infer_lines) % 3 == 0, "{}:{}".format(infer_path, len(infer_lines))
  infer_ques_num = len(infer_lines) / 3
  assert  infer_ques_num <= len(lines), "total {} source ques, but get {} pred ques".format(len(lines), infer_ques_num)
  i = 0
  j = 0
  while i < len(infer_lines):
    source = infer_lines[i]
    assert  source.strip().replace("SEQUENCE_END", "") == lines[j].strip()
    pred = infer_lines[i+1]
    i += 2
    j += 1
  if os.path.exists(ques_done_path):
    done_ques_path = ques_done_path + ".do"
  make_seq2seq_data.write_list_to_file(lines[0:j], ques_done_path)
  undo_ques = lines[j:]
  make_seq2seq_data.write_list_to_file(undo_ques, ques_path)
  if os.path.exists(infer_done_path):
    infer_done_path = infer_done_path + ".n"
  shutil.move(infer_path, infer_done_path)
  print ("move {} to {}".format(infer_path, infer_done_path))

@click.command()
@click.argument("source_prefix")
@click.argument("infer_prefix")
@click.argument("ques_done_prefix")
@click.argument("infer_done_prefix")
@click.argument("parts")
def infer_checkpoint_loop(source_prefix, infer_prefix, ques_done_prefix, infer_done_prefix, parts):
  for i in range(parts):
    source_ques_path = "{}_part_{}".format(source_prefix, i)
    infer_path = "{}_part_{}".format(infer_prefix, i)
    ques_done_path = "{}_part_{}".format(ques_done_prefix, i)
    infer_done_path = "{}_part_{}".format(infer_done_prefix, i)
    store_done_ques(source_ques_path, infer_path, ques_done_path, infer_done_path)

cli.add_command(store_done_ques)
cli.add_command(infer_checkpoint_loop)

if __name__ == "__main__":
  cli()
  # infer_checkpoint_loop()
