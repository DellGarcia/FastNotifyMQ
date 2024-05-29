prisma:
	prisma generate --schema=./app/prisma/schema.prisma
	prisma db push --schema=./app/prisma/schema.prisma