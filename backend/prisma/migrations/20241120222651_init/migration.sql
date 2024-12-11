-- CreateTable
CREATE TABLE "MusicClassification" (
    "id" SERIAL NOT NULL,
    "filename" TEXT NOT NULL,
    "model" TEXT NOT NULL,
    "genre" TEXT NOT NULL,
    "confidence" DOUBLE PRECISION NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "MusicClassification_pkey" PRIMARY KEY ("id")
);
