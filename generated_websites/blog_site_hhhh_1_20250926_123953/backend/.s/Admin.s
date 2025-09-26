lfh{path=/api/login,method=POST,auth=false}
abp{path=/api/admin/blog/posts,method=GET,auth=true}
abp{path=/api/admin/blog/posts,method=POST,auth=true}  
abp{path=/api/admin/blog/posts/{post_id},method=GET,auth=true}
abp{path=/api/admin/blog/posts/{post_id},method=PUT,auth=true}
abp{path=/api/admin/blog/posts/{post_id},method=DELETE,auth=true}
abp{path=/api/admin/blog/posts/{post_id}/publish,method=PATCH,auth=true}