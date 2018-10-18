--链接：https://github.com/hidu/mysql-schema-synic源码
在作者原来的基础上稍微修改了一些
internal/schema.go
在ParseSchema方法中增加了一句话
 if line[0] == ')' {
        fmt.Println("-----")
        break
    }
防止表存在分区是出现不能同步的现象

