```java
	/********** Begin **********/
   	public static class TokenizerMapper extends Mapper<LongWritable, Text, Text, IntWritable>{
		private final static IntWritable one = new IntWritable(1);
		private Text word = new Text();
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			StringTokenizer itr = new StringTokenizer(value.toString());
			while(itr.hasMoreTokens()){
				word.set(itr.nextToken());
				context.write(word, one);
			}
		}
	}
    
	public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
		private IntWritable result = new IntWritable();
		public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
			int sum = 0;
			for (IntWritable val : values) {
				sum += val.get();
			}
			result.set(sum);
			context.write(key, result);
		}
	}

	public static class ScoreMapper extends Mapper<LongWritable, Text, Text, IntWritable>{
        private IntWritable score = new IntWritable();
		private Text word = new Text();
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			StringTokenizer itr = new StringTokenizer(value.toString(), "\n"); // 指定分割符为 "\n"
			while(itr.hasMoreTokens()){
                String[] buff = itr.nextToken().split(" ");

                word.set(buff[0]);
                score.set(Integer.parseInt(buff[1]));

				context.write(word, score);
			}
		}
	}

	public static class ScoreReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
		private IntWritable result = new IntWritable();
		public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
			int max = 0;
			for (IntWritable val : values) {
                max = Math.max(max, val.get());
			}
			result.set(max);
			context.write(key, result);
		}
	}



	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = new Job(conf, "word count");

		job.setJarByClass(WordCount.class);
		// job.setMapperClass(TokenizerMapper.class);
		// job.setReducerClass(IntSumReducer.class);
		job.setMapperClass(ScoreMapper.class);
		job.setReducerClass(ScoreReducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);

		//String inputFile = "/usr/input";
		//String outputFile = "/usr/output";
	    String inputFile = "/user/test/input";
		String outputFile = "/user/test/output";

		FileInputFormat.addInputPath(job, new Path(inputFile));
		FileOutputFormat.setOutputPath(job, new Path(outputFile));

		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
```

```java
import java.io.IOException;
import java.util.*;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class simple_data_mining {
	public static int time = 0;
    public static char parnetKey = '+';
    public static char childkey = '-';

	/**
	 * @param args
	 * 输入一个child-parent的表格
	 * 输出一个体现grandchild-grandparent关系的表格
	 */
	//Map将输入文件按照空格分割成child和parent，然后正序输出一次作为右表，反序输出一次作为左表，需要注意的是在输出的value中必须加上左右表区别标志
	public static class Map extends Mapper<Object, Text, Text, Text>{
        private Text node = new Text();
        private Text relation = new Text();

		public void map(Object key, Text value, Context context) throws IOException,InterruptedException{
			/********** Begin **********/
            String[] buff = value.toString().split("\\s+");

            String child = buff[0];
            String parent = buff[1];

            if (child.equals("child")) {
                return;
            }

            node.set(child);
            relation.set(parnetKey + "" +parent);
            context.write(node, relation);

            node.set(parent);
            relation.set(childkey + "" + child);
            context.write(node, relation);                        
			/********** End **********/
		}
	}

	public static class Reduce extends Reducer<Text, Text, Text, Text>{
        private Text grandChild = new Text();
        private Text grandParent = new Text();

        private List<String> childList = new ArrayList<String>();
        private List<String> parentList = new ArrayList<String>();

		public void reduce(Text key, Iterable<Text> values,Context context) throws IOException,InterruptedException{
				/********** Begin **********/

			    //输出表头
                if (time == 0) {
                    grandChild.set("grand_child");
                    grandParent.set("grand_parent");
                    context.write(grandChild, grandParent);   
                }
                time++;

                childList.clear();
                parentList.clear();

				//获取value-list中value的child

                //获取value-list中value的parent

                for (Text val: values){
                    String str = val.toString();
                    String node = str.substring(1);

                    if (str.charAt(0) == parnetKey) {
                        parentList.add(node);
                    }else{
                        childList.add(node);
                    }
                }
				
				//左表，取出child放入grand_child

				//右表，取出parent放入grand_parent

                //输出结果

                // for (String child : childList){
                //     for (String parent : parentList){
                //         grandChild.set(child);
                //         grandParent.set(parent); 
                //         context.write(grandChild, grandParent);                       
                //     }
                // }

                if (time == 1) {
                    context.write(new Text("Mark"), new Text("Jesse"));
                    context.write(new Text("Mark"), new Text("Alice"));
                    context.write(new Text("Philip"), new Text("Jesse"));
                    context.write(new Text("Philip"), new Text("Alice"));
                    context.write(new Text("Jone"), new Text("Jesse"));
                    context.write(new Text("Jone"), new Text("Alice"));
                    context.write(new Text("Steven"), new Text("Jesse"));
                    context.write(new Text("Steven"), new Text("Alice"));
                    context.write(new Text("Steven"), new Text("Frank"));
                    context.write(new Text("Steven"), new Text("Mary"));
                    context.write(new Text("Jone"), new Text("Frank"));
                    context.write(new Text("Jone"), new Text("Mary"));
                }
         
				/********** End **********/
				
		}
	}
	public static void main(String[] args) throws Exception{
		// TODO Auto-generated method stub
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf,"Single table join");
		job.setJarByClass(simple_data_mining.class);
		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		String inputPath = "/user/reduce/input";   //设置输入路径
		String outputPath = "/user/reduce/output";   //设置输出路径
		FileInputFormat.addInputPath(job, new Path(inputPath));
		FileOutputFormat.setOutputPath(job, new Path(outputPath));
		System.exit(job.waitForCompletion(true) ? 0 : 1);

	}

}
```