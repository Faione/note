## MdBook

[tutorial](https://rust-lang.github.io/mdBook/)

for group in foo bar; do \
  workdir=group-$group; \
  mkdir $workdir; \
  sed -e "s/{group}/group-${group}/g" base_require.yaml > $workdir/base_require.yaml; \
  sed -e "s/{group}/group-${group}/g" default_cnp.yaml > $workdir/default_cnp.yaml; done

